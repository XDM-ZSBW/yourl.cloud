#!/usr/bin/env python3
"""
Authorized API Endpoint for Yourl.Cloud Marketing Codes
Provides secure access to marketing codes for authorized services
"""

import os
import json
import hashlib
import hmac
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, Any, List
from flask import Flask, request, jsonify, abort
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path for imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.secret_manager_client import SecretManagerClient
from scripts.database_client import DatabaseClient

app = Flask(__name__)

class AuthorizedAPI:
    def __init__(self, project_id: str, database_connection_string: Optional[str] = None):
        self.project_id = project_id
        self.secret_client = SecretManagerClient(project_id)
        self.database_client = None
        
        if database_connection_string:
            self.database_client = DatabaseClient(database_connection_string)
    
    def verify_api_key(self, api_key: str, service_name: str) -> bool:
        """Verify API key for service access"""
        if not self.database_client:
            return False
        
        try:
            # Get active authorizations
            auths = self.database_client.get_active_authorizations()
            
            for auth in auths:
                if auth['service_name'] == service_name and auth['code'] == api_key:
                    # Check if expired
                    if auth['expires_at'] and datetime.fromisoformat(auth['expires_at'].replace('Z', '+00:00')) < datetime.now(timezone.utc):
                        return False
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Error verifying API key: {e}")
            return False
    
    def get_current_code(self, service_name: str) -> Optional[str]:
        """Get current marketing code for authorized service"""
        try:
            code = self.secret_client.get_current_marketing_code()
            
            # Log usage
            if self.database_client:
                self.database_client.log_usage(
                    code=code or "unknown",
                    user_agent=request.headers.get('User-Agent'),
                    ip_address=request.remote_addr,
                    endpoint="/api/v1/current-code",
                    success=code is not None,
                    session_id=request.headers.get('X-Session-ID'),
                    device_type="api"
                )
            
            return code
        except Exception as e:
            logger.error(f"Error getting current code: {e}")
            return None
    
    def get_next_code(self, service_name: str) -> Optional[str]:
        """Get next marketing code for authorized service"""
        try:
            code = self.secret_client.get_next_marketing_code()
            
            # Log usage
            if self.database_client:
                self.database_client.log_usage(
                    code=code or "unknown",
                    user_agent=request.headers.get('User-Agent'),
                    ip_address=request.remote_addr,
                    endpoint="/api/v1/next-code",
                    success=code is not None,
                    session_id=request.headers.get('X-Session-ID'),
                    device_type="api"
                )
            
            return code
        except Exception as e:
            logger.error(f"Error getting next code: {e}")
            return None
    
    def get_code_metadata(self, service_name: str) -> Dict[str, Any]:
        """Get code metadata for authorized service"""
        try:
            metadata = self.secret_client.get_code_metadata()
            
            # Log usage
            if self.database_client:
                self.database_client.log_usage(
                    code="metadata",
                    user_agent=request.headers.get('User-Agent'),
                    ip_address=request.remote_addr,
                    endpoint="/api/v1/metadata",
                    success=True,
                    session_id=request.headers.get('X-Session-ID'),
                    device_type="api"
                )
            
            return metadata
        except Exception as e:
            logger.error(f"Error getting code metadata: {e}")
            return {}

# Initialize API
api = AuthorizedAPI(
    project_id=os.environ.get('GOOGLE_CLOUD_PROJECT', 'root-wharf-383822'),
    database_connection_string=os.environ.get('DATABASE_CONNECTION_STRING')
)

@app.route('/api/v1/current-code', methods=['GET'])
def get_current_code():
    """Get current marketing code (requires authorization)"""
    # Verify authorization
    api_key = request.headers.get('X-API-Key')
    service_name = request.headers.get('X-Service-Name')
    
    if not api_key or not service_name:
        abort(401, description="Missing API key or service name")
    
    if not api.verify_api_key(api_key, service_name):
        abort(403, description="Invalid API key or unauthorized service")
    
    # Get current code
    code = api.get_current_code(service_name)
    
    if code:
        return jsonify({
            "status": "success",
            "code": code,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": service_name
        })
    else:
        abort(500, description="Failed to retrieve current code")

@app.route('/api/v1/next-code', methods=['GET'])
def get_next_code():
    """Get next marketing code (requires authorization)"""
    # Verify authorization
    api_key = request.headers.get('X-API-Key')
    service_name = request.headers.get('X-Service-Name')
    
    if not api_key or not service_name:
        abort(401, description="Missing API key or service name")
    
    if not api.verify_api_key(api_key, service_name):
        abort(403, description="Invalid API key or unauthorized service")
    
    # Get next code
    code = api.get_next_code(service_name)
    
    if code:
        return jsonify({
            "status": "success",
            "code": code,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": service_name
        })
    else:
        abort(500, description="Failed to retrieve next code")

@app.route('/api/v1/metadata', methods=['GET'])
def get_metadata():
    """Get code metadata (requires authorization)"""
    # Verify authorization
    api_key = request.headers.get('X-API-Key')
    service_name = request.headers.get('X-Service-Name')
    
    if not api_key or not service_name:
        abort(401, description="Missing API key or service name")
    
    if not api.verify_api_key(api_key, service_name):
        abort(403, description="Invalid API key or unauthorized service")
    
    # Get metadata
    metadata = api.get_code_metadata(service_name)
    
    if metadata:
        return jsonify({
            "status": "success",
            "metadata": metadata,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": service_name
        })
    else:
        abort(500, description="Failed to retrieve metadata")

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "project_id": api.project_id
    })

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "error": "Unauthorized",
        "message": error.description,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "error": "Forbidden",
        "message": error.description,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 403

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": error.description,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
