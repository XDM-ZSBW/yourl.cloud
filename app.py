#!/usr/bin/env python3
"""
Simple API Server with Visual Inspection and Google Cloud Run Support
====================================================================

A self-executing Python Flask application that responds with the request URL
and provides visual inspection capabilities for PC and phone devices.
Enhanced for Google Cloud Run deployment with dual-mode endpoint support.
Production-ready with WSGI server support.

Author: Yourl Cloud Inc.
Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
Friends and Family Guard: Enabled
Google Cloud Run: Supported
WSGI Server: Production Ready
Domain Mapping: Compatible
"""

from flask import Flask, request, jsonify, render_template_string, render_template
import socket
import os
import re
import logging
import platform
import subprocess
import sys
import webbrowser
import threading
import time
import hashlib
import random
from datetime import datetime
from urllib.parse import urlparse

# Configure logging for production cloud environments
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration - Google Cloud Run compatible with domain mapping support
HOST = '0.0.0.0'  # Listen on all interfaces (required for Cloud Run)

# Port configuration - Use random available port for local development, 8080 for production
if os.environ.get('PORT'):
    # Production environment (Cloud Run) - use environment PORT
    PORT = int(os.environ.get('PORT', 8080))
else:
    # Local development - use random available port
    import socket
    def find_free_port():
        """Find a free port to use for local development"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))  # Bind to any available port
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    PORT = find_free_port()

DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
# Production mode detection - All instances deploy as production instances
PRODUCTION = True  # Always production for all deployments

# Cloud Run Domain Mapping Configuration
# These settings ensure compatibility with custom domain mappings
CLOUD_RUN_CONFIG = {
    "domain_mapping_enabled": True,
    "region": "us-west1",  # Default region for domain mappings
    "trust_proxy": True,  # Trust X-Forwarded headers from Cloud Run proxy
    "cors_enabled": True,  # Enable CORS for domain mapping compatibility
    "health_check_path": "/health",  # Health check endpoint for Cloud Run
    "readiness_check_path": "/health"  # Readiness check endpoint
}

def generate_marketing_password():
    """
    Generate a fun, marketing-friendly password that changes with each commit.
    Uses git commit hash to ensure consistency within a commit but changes between commits.
    Only uses basic ASCII characters for maximum compatibility.
    """
    try:
        # Get the current git commit hash
        commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], 
                                            text=True, stderr=subprocess.DEVNULL).strip()[:8]
    except:
        # Fallback if git is not available
        commit_hash = hashlib.md5(str(datetime.utcnow()).encode()).hexdigest()[:8]
    
    # Fun marketing words and phrases (ASCII only)
    marketing_words = [
        "CLOUD", "FUTURE", "INNOVATE", "DREAM", "BUILD", "CREATE", "LAUNCH", "FLY",
        "SPARK", "SHINE", "GLOW", "RISE", "LEAP", "JUMP", "DASH", "ZOOM",
        "POWER", "MAGIC", "WONDER", "AMAZE", "THRILL", "EXCITE", "INSPIRE", "IGNITE",
        "ROCKET", "STAR", "MOON", "SUN", "OCEAN", "MOUNTAIN", "FOREST", "RIVER",
        "TECH", "AI", "CODE", "DATA", "SMART", "FAST", "SECURE", "TRUST",
        "FRIEND", "FAMILY", "TEAM", "SQUAD", "CREW", "GANG", "TRIBE", "CLAN"
    ]
    
    # Fun ASCII symbols and characters
    ascii_symbols = ["!", "@", "#", "$", "%", "&", "*", "+", "=", "?", "~", "^"]
    
    # Generate a deterministic but fun password using the commit hash
    # Convert commit hash to a number for seeding
    hash_num = int(commit_hash, 16)
    random.seed(hash_num)
    
    # Pick a random marketing word
    word = random.choice(marketing_words)
    
    # Pick a random ASCII symbol
    symbol = random.choice(ascii_symbols)
    
    # Generate a short number (2-3 digits)
    number = random.randint(10, 999)
    
    # Combine them in a fun way (ASCII only)
    password = f"{word}{number}{symbol}"
    
    return password

def get_current_marketing_password():
    """
    Get the current live marketing password (for Perplexity/landing page display).
    This should only change after successful deployment.
    """
    try:
        from scripts.marketing_code_manager import MarketingCodeManager
        manager = MarketingCodeManager(os.environ.get('GOOGLE_CLOUD_PROJECT', 'root-wharf-383822'))
        return manager.get_live_experience_code()
    except Exception as e:
        # Fallback to environment variable or generate based on commit
        build_password = os.environ.get('BUILD_MARKETING_PASSWORD')
        if build_password:
            return build_password
        
        # Last resort: generate based on current commit
        return generate_marketing_password()

def get_next_marketing_password():
    """
    Get the next marketing password (for Cursor/authenticated users).
    This is what will become the current code after next deployment.
    """
    try:
        from scripts.marketing_code_manager import MarketingCodeManager
        manager = MarketingCodeManager(os.environ.get('GOOGLE_CLOUD_PROJECT', 'root-wharf-383822'))
        return manager.get_next_build_code()
    except Exception as e:
        # Fallback: generate next code based on current commit
        try:
            commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], 
                                                text=True, stderr=subprocess.DEVNULL).strip()[:8]
            next_hash = commit_hash + "next"
        except:
            next_hash = "next_unknown"
        
        return generate_marketing_password_from_hash(next_hash)

def generate_marketing_password_from_hash(commit_hash: str):
    """Generate marketing password from specific commit hash"""
    # Fun marketing words and phrases (ASCII only)
    marketing_words = [
        "CLOUD", "FUTURE", "INNOVATE", "DREAM", "BUILD", "CREATE", "LAUNCH", "FLY",
        "SPARK", "SHINE", "GLOW", "RISE", "LEAP", "JUMP", "DASH", "ZOOM",
        "POWER", "MAGIC", "WONDER", "AMAZE", "THRILL", "EXCITE", "INSPIRE", "IGNITE",
        "ROCKET", "STAR", "MOON", "SUN", "OCEAN", "MOUNTAIN", "FOREST", "RIVER",
        "TECH", "AI", "CODE", "DATA", "SMART", "FAST", "SECURE", "TRUST",
        "FRIEND", "FAMILY", "TEAM", "SQUAD", "CREW", "GANG", "TRIBE", "CLAN"
    ]
    
    # Fun ASCII symbols and characters
    ascii_symbols = ["!", "@", "#", "$", "%", "&", "*", "+", "=", "?", "~", "^"]
    
    # Generate a deterministic but fun password using the commit hash
    hash_num = int(commit_hash, 16) if commit_hash != "unknown" else hash(commit_hash)
    random.seed(hash_num)
    
    # Pick a random marketing word
    word = random.choice(marketing_words)
    
    # Pick a random ASCII symbol
    symbol = random.choice(ascii_symbols)
    
    # Generate a short number (2-3 digits)
    number = random.randint(10, 999)
    
    # Combine them in a fun way (ASCII only)
    password = f"{word}{number}{symbol}"
    
    return password

# Friends and Family Guard Ruleset
FRIENDS_FAMILY_GUARD = {
    "enabled": True,
    "visual_inspection": {
        "pc_allowed": True,
        "phone_allowed": True,
        "watch_blocked": True,
        "tablet_allowed": True
    },
    "session_id": "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49",
    "organization": "Yourl Cloud Inc."
}

# Demo configuration for rapid prototyping (replace with proper auth/db for production)
DEMO_CONFIG = {
    "password": get_current_marketing_password(),  # Dynamic marketing password that changes with commits
    "connections": [
        {
            "id": 1,
            "name": "GitHub Repository",
            "url": "https://github.com/XDM-ZSBW/yourl.cloud",
            "description": "Source code and documentation"
        },
        {
            "id": 2,
            "name": "Google Cloud Run",
            "url": "https://cloud.google.com/run",
            "description": "Deploy and scale applications"
        },
        {
            "id": 3,
            "name": "Flask Framework",
            "url": "https://flask.palletsprojects.com/",
            "description": "Python web framework"
        },
        {
            "id": 4,
            "name": "Perplexity AI",
            "url": "https://perplexity.ai",
            "description": "AI-powered search and assistance"
        },
        {
            "id": 5,
            "name": "Cursor IDE",
            "url": "https://cursor.sh",
            "description": "AI-powered code editor"
        }
    ]
}

# Configure Flask for Cloud Run domain mapping compatibility
app.config.update(
    # Trust X-Forwarded headers from Cloud Run proxy
    PREFERRED_URL_SCHEME='https',  # Cloud Run always serves HTTPS
    # Enable proxy support for X-Forwarded headers
    USE_X_SENDFILE=False,
    # Disable strict host checking for domain mapping compatibility
    SERVER_NAME=None
)

def get_client_ip():
    """
    Get the real client IP address, handling Cloud Run's X-Forwarded headers.
    Cloud Run sits behind a proxy, so we need to check X-Forwarded-For header.
    """
    # Check for X-Forwarded-For header (Cloud Run proxy)
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        # X-Forwarded-For can contain multiple IPs, take the first one
        return x_forwarded_for.split(',')[0].strip()
    # Fallback to direct connection
    return request.remote_addr

def get_original_host():
    """
    Get the original host from X-Forwarded-Host header (Cloud Run domain mapping).
    Falls back to the request host if not available.
    """
    return request.headers.get('X-Forwarded-Host', request.host)

def get_original_protocol():
    """
    Get the original protocol from X-Forwarded-Proto header.
    Cloud Run always serves HTTPS, but we check the header for completeness.
    """
    return request.headers.get('X-Forwarded-Proto', 'https')

def detect_device_type(user_agent):
    """
    Detect device type based on User-Agent string.
    Returns: 'pc', 'phone', 'tablet', 'watch', 'unknown'
    """
    ua_lower = user_agent.lower()
    
    # Watch detection (blocked for visual inspection)
    if any(keyword in ua_lower for keyword in ['watch', 'wearable', 'smartwatch', 'apple watch', 'samsung gear']):
        return 'watch'
    
    # Phone detection
    if any(keyword in ua_lower for keyword in ['mobile', 'android', 'iphone', 'phone', 'blackberry']):
        return 'phone'
    
    # Tablet detection
    if any(keyword in ua_lower for keyword in ['tablet', 'ipad', 'android']):
        return 'tablet'
    
    # Default to PC
    return 'pc'

def is_visual_inspection_allowed(device_type):
    """
    Check if visual inspection is allowed for the given device type.
    """
    if not FRIENDS_FAMILY_GUARD["enabled"]:
        return True
    
    return FRIENDS_FAMILY_GUARD["visual_inspection"].get(f"{device_type}_allowed", False)

@app.route('/', methods=['GET', 'POST'])
def main_endpoint():
    """
    Main endpoint that handles both GET (landing page) and POST (authentication).
    Compatible with Cloud Run domain mappings.
    """
    if request.method == 'GET':
        # Get current marketing password
        current_password = get_current_marketing_password()
        
        # Return the landing page
        return render_template('index.html') if os.path.exists('templates/index.html') else f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Yourl.Cloud - URL API Server</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; text-align: center; }}
                .form-group {{ margin: 20px 0; }}
                label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
                input[type="password"] {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }}
                button {{ background: #007bff; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }}
                button:hover {{ background: #0056b3; }}
                .info {{ background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .password-display {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; margin: 10px 0; text-align: center; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Yourl.Cloud</h1>
                <div class="info">
                    <strong>URL API Server with Visual Inspection</strong><br>
                    Production-ready Flask application with security features.<br>
                    <strong>Domain:</strong> {get_original_host()}<br>
                    <strong>Protocol:</strong> {get_original_protocol()}
                </div>
                <form method="POST">
                    <div class="form-group">
                        <label for="password">🎯 Marketing Password:</label>
                        <input type="password" id="password" name="password" placeholder="Enter the fun marketing password" required>
                    </div>
                    <button type="submit">🚀 Launch Experience</button>
                </form>
                <div class="password-display">
                    <strong>🎪 Current Marketing Password:</strong> {current_password}
                </div>
                <div class="info">
                    <strong>Health Check:</strong> <a href="/health">/health</a><br>
                    <strong>Status:</strong> <a href="/status">/status</a>
                </div>
            </div>
        </body>
        </html>
        """
    
    elif request.method == 'POST':
        # Handle authentication with simple password check
        password = request.form.get('password', '')
        current_password = get_current_marketing_password()
        
        if password == current_password:
            # Get the next code for authenticated users (Cursor ownership)
            next_password = get_next_marketing_password()
            return jsonify({
                "status": "authenticated",
                "message": "🎉 Welcome to Yourl.Cloud API! Marketing password accepted!",
                "connections": DEMO_CONFIG["connections"],
                "timestamp": datetime.utcnow().isoformat(),
                "organization": FRIENDS_FAMILY_GUARD["organization"],
                "domain": get_original_host(),
                "protocol": get_original_protocol(),
                "current_marketing_password": current_password,
                "next_marketing_password": next_password,
                "ownership": {
                    "perplexity": "current_marketing_password",
                    "cursor": "next_marketing_password"
                }
            })
        else:
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Access Denied - Yourl.Cloud</title>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; text-align: center; }}
                    .container {{ max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    h1 {{ color: #d32f2f; }}
                    .btn {{ background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }}
                    .password-hint {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>❌ Access Denied</h1>
                    <p>Invalid marketing password. Please try again.</p>
                    <div class="password-hint">
                        <strong>💡 Hint:</strong> The current marketing password is: {current_password}
                    </div>
                    <a href="/" class="btn">🔄 Try Again</a>
                </div>
            </body>
            </html>
            """
    
    else:
        return jsonify({"error": "Method not allowed"}), 405

@app.route('/api', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def get_request_url():
    """
    API endpoint that returns the request URL and metadata.
    Compatible with Cloud Run domain mappings.
    """
    # Get request information with Cloud Run header support
    url = request.url
    method = request.method
    headers = dict(request.headers)
    user_agent = headers.get('User-Agent', 'Unknown')
    device_type = detect_device_type(user_agent)
    
    # Get Cloud Run specific information
    client_ip = get_client_ip()
    original_host = get_original_host()
    original_protocol = get_original_protocol()
    
    # Check if visual inspection is allowed
    if is_visual_inspection_allowed(device_type):
        # Return HTML for allowed devices
        return render_visual_inspection(url, device_type, datetime.utcnow(), original_host, original_protocol)
    else:
        # Return JSON for blocked devices (like watches)
        return jsonify({
            "url": url,
            "method": method,
            "device_type": device_type,
            "visual_inspection": "blocked",
            "timestamp": datetime.utcnow().isoformat(),
            "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"],
            "organization": FRIENDS_FAMILY_GUARD["organization"],
            "cloud_run": {
                "client_ip": client_ip,
                "original_host": original_host,
                "original_protocol": original_protocol,
                "domain_mapping_enabled": CLOUD_RUN_CONFIG["domain_mapping_enabled"]
            }
        })

def render_visual_inspection(url, device_type, timestamp, original_host, original_protocol):
    """
    Render the visual inspection interface for allowed devices.
    Enhanced for Cloud Run domain mapping compatibility.
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yourl.Cloud - Visual Inspection</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #007bff, #0056b3);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 2.5em;
                font-weight: 300;
            }}
            .content {{
                padding: 30px;
            }}
            .url-display {{
                background: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                word-break: break-all;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }}
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .info-card {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                border-left: 4px solid #007bff;
            }}
            .info-card h3 {{
                margin: 0 0 10px 0;
                color: #007bff;
            }}
            .status-badge {{
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
            }}
            .status-success {{
                background: #d4edda;
                color: #155724;
            }}
            .status-info {{
                background: #d1ecf1;
                color: #0c5460;
            }}
            .refresh-btn {{
                background: linear-gradient(135deg, #007bff, #0056b3);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                transition: transform 0.2s;
            }}
            .refresh-btn:hover {{
                transform: translateY(-2px);
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                border-top: 1px solid #e9ecef;
            }}
            @media (max-width: 768px) {{
                .container {{
                    margin: 10px;
                    border-radius: 10px;
                }}
                .header h1 {{
                    font-size: 2em;
                }}
                .content {{
                    padding: 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔍 Visual Inspection</h1>
                <p>Yourl.Cloud URL API Server - Real-time Monitoring</p>
            </div>
            
            <div class="content">
                <div class="url-display">
                    <strong>Request URL:</strong><br>
                    {url}
                </div>
                
                <div class="info-grid">
                    <div class="info-card">
                        <h3>📱 Device Information</h3>
                        <p><strong>Type:</strong> {device_type.title()}</p>
                        <p><strong>Status:</strong> <span class="status-badge status-success">Allowed</span></p>
                    </div>
                    
                    <div class="info-card">
                        <h3>🛡️ Security Status</h3>
                        <p><strong>Guard:</strong> <span class="status-badge status-success">Enabled</span></p>
                        <p><strong>Inspection:</strong> <span class="status-badge status-info">Active</span></p>
                    </div>
                    
                    <div class="info-card">
                        <h3>⏰ Timestamp</h3>
                        <p><strong>Time:</strong> {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                        <p><strong>Session:</strong> {FRIENDS_FAMILY_GUARD['session_id'][:8]}...</p>
                    </div>
                    
                    <div class="info-card">
                        <h3>🏢 Organization</h3>
                        <p><strong>Company:</strong> {FRIENDS_FAMILY_GUARD['organization']}</p>
                        <p><strong>Environment:</strong> <span class="status-badge status-success">Production</span></p>
                    </div>
                    
                    <div class="info-card">
                        <h3>☁️ Cloud Run Info</h3>
                        <p><strong>Domain:</strong> {original_host}</p>
                        <p><strong>Protocol:</strong> {original_protocol}</p>
                        <p><strong>Mapping:</strong> <span class="status-badge status-success">Enabled</span></p>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <button class="refresh-btn" onclick="location.reload()">
                        🔄 Refresh Data
                    </button>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>Yourl.Cloud</strong> - Secure URL API Server with Visual Inspection</p>
                <p>Session: {FRIENDS_FAMILY_GUARD['session_id']} | Organization: {FRIENDS_FAMILY_GUARD['organization']}</p>
            </div>
        </div>
        
        <script>
            // Auto-refresh every 30 seconds
            setTimeout(function() {{
                location.reload();
            }}, 30000);
        </script>
    </body>
    </html>
    """
    return html_content

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for Cloud Run domain mapping compatibility.
    This endpoint is used by Cloud Run for health checks and domain mapping validation.
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "url-api",
        "version": "1.0.0",
        "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"],
        "cloud_run_support": True,
        "domain_mapping": {
            "enabled": CLOUD_RUN_CONFIG["domain_mapping_enabled"],
            "region": CLOUD_RUN_CONFIG["region"],
            "health_check_path": CLOUD_RUN_CONFIG["health_check_path"]
        },
        "wsgi_server": "waitress" if platform.system() == "Windows" else "gunicorn",
        "production_mode": True,
        "deployment_model": "all_instances_production",
        "port": PORT,
        "host": get_original_host(),
        "protocol": get_original_protocol()
    })

@app.route('/status', methods=['GET'])
def status():
    """
    Status endpoint with service information.
    Enhanced for Cloud Run domain mapping compatibility.
    """
    return jsonify({
        "service": "URL API with Visual Inspection",
        "version": "1.0.0",
        "status": "running",
        "port": PORT,
        "host": get_original_host(),
        "timestamp": datetime.utcnow().isoformat(),
        "session_id": FRIENDS_FAMILY_GUARD["session_id"],
        "organization": FRIENDS_FAMILY_GUARD["organization"],
        "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"],
        "visual_inspection": FRIENDS_FAMILY_GUARD["visual_inspection"],
        "cloud_run_support": True,
        "demo_mode": True,
        "wsgi_server": "waitress" if platform.system() == "Windows" else "gunicorn",
        "production_mode": True,
        "deployment_model": "all_instances_production",
        "domain_mapping": {
            "enabled": CLOUD_RUN_CONFIG["domain_mapping_enabled"],
            "region": CLOUD_RUN_CONFIG["region"],
            "original_host": get_original_host(),
            "original_protocol": get_original_protocol(),
            "client_ip": get_client_ip()
        }
    })

@app.route('/guard', methods=['GET'])
def guard_status():
    """
    Friends and Family Guard status endpoint.
    """
    return jsonify({
        "friends_family_guard": FRIENDS_FAMILY_GUARD,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors by returning the request URL.
    Compatible with Cloud Run domain mappings.
    """
    return jsonify({
        "error": "Not Found",
        "url": request.url,
        "message": "The requested resource was not found, but here's your request URL",
        "timestamp": datetime.utcnow().isoformat(),
        "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"],
        "cloud_run": {
            "original_host": get_original_host(),
            "original_protocol": get_original_protocol()
        }
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors.
    """
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "error": "Internal Server Error",
        "url": request.url,
        "message": "An internal server error occurred",
        "timestamp": datetime.utcnow().isoformat(),
        "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"]
    }), 500

def launch_browser(url, delay=1.5):
    """
    Launch the default browser to the specified URL after a short delay.
    This allows the server to start up before the browser tries to connect.
    """
    def _launch():
        time.sleep(delay)  # Wait for server to start
        try:
            webbrowser.open(url)
            print(f"🌐 Browser launched: {url}")
        except Exception as e:
            print(f"⚠️ Could not launch browser: {e}")
    
    # Launch browser in a separate thread to avoid blocking
    browser_thread = threading.Thread(target=_launch, daemon=True)
    browser_thread.start()

def start_production_server():
    """
    Start the application using a production WSGI server.
    Enhanced for Cloud Run domain mapping compatibility.
    """
    print("🚀 Starting production WSGI server...")
    
    if platform.system() == "Windows":
        # Use Waitress on Windows
        try:
            import waitress
            print("✅ Using Waitress WSGI server (Windows)")
            # Suppress Waitress logging messages
            import logging
            logging.getLogger('waitress').setLevel(logging.ERROR)
            waitress.serve(app, host=HOST, port=PORT, threads=4, connection_limit=1000)
        except ImportError:
            print("❌ Waitress not found. Installing...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "waitress"], check=True)
                import waitress
                print("✅ Waitress installed - starting production server...")
                # Suppress Waitress logging messages
                import logging
                logging.getLogger('waitress').setLevel(logging.ERROR)
                waitress.serve(app, host=HOST, port=PORT, threads=4, connection_limit=1000)
            except Exception as e:
                print(f"❌ Failed to install/use Waitress: {e}")
                print("🔄 Falling back to Flask development server...")
                app.run(host=HOST, port=PORT, debug=False, threaded=True)
    else:
        # Use Gunicorn on Unix-like systems
        try:
            import gunicorn
            print("✅ Using Gunicorn WSGI server (Unix)")
            cmd = ["gunicorn", "--bind", f"{HOST}:{PORT}", "--workers", "4", "app:app"]
            subprocess.run(cmd, check=True)
        except ImportError:
            print("❌ Gunicorn not found. Installing...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "gunicorn"], check=True)
                import gunicorn
                print("✅ Gunicorn installed - starting production server...")
                cmd = ["gunicorn", "--bind", f"{HOST}:{PORT}", "--workers", "4", "app:app"]
                subprocess.run(cmd, check=True)
            except Exception as e:
                print(f"❌ Failed to install/use Gunicorn: {e}")
                print("🔄 Falling back to Flask development server...")
                app.run(host=HOST, port=PORT, debug=False, threaded=True)

if __name__ == '__main__':
    # Determine the display address for users
    if HOST == '0.0.0.0':
        display_host = 'localhost'  # More user-friendly than 0.0.0.0
    else:
        display_host = HOST
    
    # Get current marketing password
    current_password = get_current_marketing_password()
    
    print(f"🚀 Starting URL API Server with Visual Inspection")
    print(f"📍 Host: {display_host}")
    print(f"🐛 Debug: {DEBUG}")
    print(f"🏭 Production: {PRODUCTION} (All instances are production instances)")
    print(f"🆔 Session: {FRIENDS_FAMILY_GUARD['session_id']}")
    print(f"🏢 Organization: {FRIENDS_FAMILY_GUARD['organization']}")
    print(f"🛡️ Friends and Family Guard: {'Enabled' if FRIENDS_FAMILY_GUARD['enabled'] else 'Disabled'}")
    print(f"👁️ Visual Inspection: PC/Phone/Tablet allowed, Watch blocked")
    print(f"☁️ Google Cloud Run Support: Enabled")
    print(f"🌐 Domain Mapping: {'Enabled' if CLOUD_RUN_CONFIG['domain_mapping_enabled'] else 'Disabled'}")
    print(f"🎪 Marketing Password: {current_password}")
    print("=" * 60)
    
    # Launch browser for local development (not for production/Cloud Run)
    if not os.environ.get('PORT'):
        local_url = f"http://{display_host}:{PORT}"
        print(f"🌐 Launching browser to: {local_url}")
        launch_browser(local_url)
    
    # Start with production WSGI server
    start_production_server()
