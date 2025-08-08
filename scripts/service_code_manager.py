#!/usr/bin/env python3
"""
Service Code Manager for Yourl.Cloud
Manages marketing codes for different services and future extensibility
"""

import os
import json
import hashlib
import subprocess
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.marketing_code_manager import MarketingCodeManager

class ServiceCodeManager:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.services_file = "codes/service_codes.json"
        self._ensure_codes_directory()
    
    def _ensure_codes_directory(self):
        """Ensure the codes directory exists"""
        os.makedirs("codes", exist_ok=True)
    
    def create_service_code(self, service_name: str, service_type: str, owner: str) -> str:
        """
        Create a new marketing code for a specific service.
        
        Args:
            service_name: Name of the service (e.g., 'backend-api', 'frontend-dashboard')
            service_type: Type of service (e.g., 'backend', 'frontend', 'api')
            owner: Owner of the service (e.g., 'cursor', 'perplexity', 'custom')
        
        Returns:
            Generated marketing code for the service
        """
        try:
            with open(self.services_file, 'r') as f:
                services_data = json.load(f)
        except FileNotFoundError:
            services_data = {'services': []}
        
        # Generate unique code for this service
        service_code = self._generate_service_code(service_name, service_type)
        
        # Create service record
        service_record = {
            'service_name': service_name,
            'service_type': service_type,
            'owner': owner,
            'code': service_code,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'status': 'active',
            'project_id': self.project_id
        }
        
        services_data['services'].append(service_record)
        
        with open(self.services_file, 'w') as f:
            json.dump(services_data, f, indent=2)
        
        return service_code
    
    def _generate_service_code(self, service_name: str, service_type: str) -> str:
        """Generate a unique marketing code for a service"""
        # Create a unique seed based on service name and type
        seed_string = f"{service_name}:{service_type}:{self.project_id}"
        seed_hash = hashlib.sha256(seed_string.encode()).hexdigest()[:8]
        
        # Use the marketing code manager to generate the code
        manager = MarketingCodeManager(self.project_id)
        return manager._generate_build_code(seed_hash)
    
    def get_service_code(self, service_name: str) -> Optional[str]:
        """Get the marketing code for a specific service"""
        try:
            with open(self.services_file, 'r') as f:
                services_data = json.load(f)
            
            for service in services_data.get('services', []):
                if service['service_name'] == service_name and service['status'] == 'active':
                    return service['code']
        except FileNotFoundError:
            pass
        
        return None
    
    def list_active_services(self) -> List[Dict[str, Any]]:
        """List all active services and their codes"""
        try:
            with open(self.services_file, 'r') as f:
                services_data = json.load(f)
            
            return [service for service in services_data.get('services', []) 
                   if service['status'] == 'active']
        except FileNotFoundError:
            return []
    
    def deactivate_service(self, service_name: str) -> bool:
        """Deactivate a service code"""
        try:
            with open(self.services_file, 'r') as f:
                services_data = json.load(f)
            
            for service in services_data.get('services', []):
                if service['service_name'] == service_name:
                    service['status'] = 'inactive'
                    service['deactivated_at'] = datetime.now(timezone.utc).isoformat()
                    
                    with open(self.services_file, 'w') as f:
                        json.dump(services_data, f, indent=2)
                    
                    return True
        except FileNotFoundError:
            pass
        
        return False
    
    def get_service_audit_trail(self, service_name: str) -> List[Dict[str, Any]]:
        """Get audit trail for a specific service"""
        try:
            with open(self.services_file, 'r') as f:
                services_data = json.load(f)
            
            return [service for service in services_data.get('services', []) 
                   if service['service_name'] == service_name]
        except FileNotFoundError:
            return []

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Service Code Manager")
    parser.add_argument("--project", required=True, help="Google Cloud project ID")
    parser.add_argument("--action", choices=['create', 'get', 'list', 'deactivate', 'audit'],
                       required=True, help="Action to perform")
    parser.add_argument("--service-name", help="Service name")
    parser.add_argument("--service-type", help="Service type")
    parser.add_argument("--owner", help="Service owner")
    
    args = parser.parse_args()
    
    manager = ServiceCodeManager(args.project)
    
    if args.action == 'create':
        if not all([args.service_name, args.service_type, args.owner]):
            parser.error("--service-name, --service-type, and --owner are required for create action")
        
        code = manager.create_service_code(args.service_name, args.service_type, args.owner)
        print(f"Created service code: {code}")
        
    elif args.action == 'get':
        if not args.service_name:
            parser.error("--service-name is required for get action")
        
        code = manager.get_service_code(args.service_name)
        if code:
            print(f"Service code for {args.service_name}: {code}")
        else:
            print(f"No active code found for service: {args.service_name}")
            
    elif args.action == 'list':
        services = manager.list_active_services()
        print("Active Services:")
        for service in services:
            print(f"  {service['service_name']} ({service['service_type']}) - {service['code']} - Owner: {service['owner']}")
            
    elif args.action == 'deactivate':
        if not args.service_name:
            parser.error("--service-name is required for deactivate action")
        
        if manager.deactivate_service(args.service_name):
            print(f"Deactivated service: {args.service_name}")
        else:
            print(f"Service not found: {args.service_name}")
            
    elif args.action == 'audit':
        if not args.service_name:
            parser.error("--service-name is required for audit action")
        
        audit_trail = manager.get_service_audit_trail(args.service_name)
        print(f"Audit trail for {args.service_name}:")
        for record in audit_trail:
            print(f"  {record['created_at']} - {record['code']} - Status: {record['status']}")
