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
"""

from flask import Flask, request, jsonify, render_template_string, render_template
import socket
import os
import re
import logging
from datetime import datetime
from urllib.parse import urlparse

# Configure logging for production cloud environments
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration - Google Cloud Run compatible
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = int(os.environ.get('PORT', 8080))  # Read PORT from environment (default 8080 for Cloud Run)
DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
# Production mode detection - All instances deploy as production instances
PRODUCTION = True  # Always production for all deployments

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
    "password": "yourl2024",  # Hardcoded demo password
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
        }
    ]
}

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
    """
    if request.method == 'GET':
        # Return the landing page
        return render_template('index.html') if os.path.exists('templates/index.html') else """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Yourl.Cloud - URL API Server</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #333; text-align: center; }
                .form-group { margin: 20px 0; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
                button { background: #007bff; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
                button:hover { background: #0056b3; }
                .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Yourl.Cloud</h1>
                <div class="info">
                    <strong>URL API Server with Visual Inspection</strong><br>
                    Production-ready Flask application with security features.
                </div>
                <form method="POST">
                    <div class="form-group">
                        <label for="password">Demo Password:</label>
                        <input type="password" id="password" name="password" placeholder="Enter demo password" required>
                    </div>
                    <button type="submit">Access API</button>
                </form>
                <div class="info">
                    <strong>Demo Password:</strong> yourl2024<br>
                    <strong>Health Check:</strong> <a href="/health">/health</a><br>
                    <strong>Status:</strong> <a href="/status">/status</a>
                </div>
            </div>
        </body>
        </html>
        """
    
    elif request.method == 'POST':
        # Handle authentication
        password = request.form.get('password', '')
        
        if password == DEMO_CONFIG["password"]:
            return jsonify({
                "status": "authenticated",
                "message": "Welcome to Yourl.Cloud API",
                "connections": DEMO_CONFIG["connections"],
                "timestamp": datetime.utcnow().isoformat(),
                "organization": FRIENDS_FAMILY_GUARD["organization"]
            })
        else:
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Access Denied - Yourl.Cloud</title>
                <meta charset="utf-8">
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; text-align: center; }
                    .container { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h1 { color: #d32f2f; }
                    .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>❌ Access Denied</h1>
                    <p>Invalid password. Please try again.</p>
                    <a href="/" class="btn">Go Back</a>
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
    """
    # Get request information
    url = request.url
    method = request.method
    headers = dict(request.headers)
    user_agent = headers.get('User-Agent', 'Unknown')
    device_type = detect_device_type(user_agent)
    
    # Check if visual inspection is allowed
    if is_visual_inspection_allowed(device_type):
        # Return HTML for allowed devices
        return render_visual_inspection(url, device_type, datetime.utcnow())
    else:
        # Return JSON for blocked devices (like watches)
        return jsonify({
            "url": url,
            "method": method,
            "device_type": device_type,
            "visual_inspection": "blocked",
            "timestamp": datetime.utcnow().isoformat(),
            "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"],
            "organization": FRIENDS_FAMILY_GUARD["organization"]
        })

def render_visual_inspection(url, device_type, timestamp):
    """
    Render the visual inspection interface for allowed devices.
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
    Health check endpoint for Cloud Run.
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "url-api",
        "version": "1.0.0",
        "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"],
        "cloud_run_support": True,
        "wsgi_server": "flask",
        "production_mode": True,
        "deployment_model": "all_instances_production",
        "port": PORT
    })

@app.route('/status', methods=['GET'])
def status():
    """
    Status endpoint with service information.
    """
    return jsonify({
        "service": "URL API with Visual Inspection",
        "version": "1.0.0",
        "status": "running",
        "port": PORT,
        "host": HOST,
        "timestamp": datetime.utcnow().isoformat(),
        "session_id": FRIENDS_FAMILY_GUARD["session_id"],
        "organization": FRIENDS_FAMILY_GUARD["organization"],
        "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"],
        "visual_inspection": FRIENDS_FAMILY_GUARD["visual_inspection"],
        "cloud_run_support": True,
        "demo_mode": True,
        "wsgi_server": "flask",
        "production_mode": True,
        "deployment_model": "all_instances_production"
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
    """
    return jsonify({
        "error": "Not Found",
        "url": request.url,
        "message": "The requested resource was not found, but here's your request URL",
        "timestamp": datetime.utcnow().isoformat(),
        "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"]
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

if __name__ == '__main__':
    print(f"🚀 Starting URL API Server with Visual Inspection")
    print(f"📍 Host: {HOST}")
    print(f"🔌 Port: {PORT}")
    print(f"🐛 Debug: {DEBUG}")
    print(f"🏭 Production: {PRODUCTION} (All instances are production instances)")
    print(f"🆔 Session: {FRIENDS_FAMILY_GUARD['session_id']}")
    print(f"🏢 Organization: {FRIENDS_FAMILY_GUARD['organization']}")
    print(f"🛡️ Friends and Family Guard: {'Enabled' if FRIENDS_FAMILY_GUARD['enabled'] else 'Disabled'}")
    print(f"👁️ Visual Inspection: PC/Phone/Tablet allowed, Watch blocked")
    print(f"☁️ Google Cloud Run Support: Enabled (PORT={PORT})")
    print(f"🔐 Demo Mode: Enabled (password: {DEMO_CONFIG['password']})")
    print(f"🌐 Access: http://{HOST}:{PORT}")
    print("=" * 60)
    
    # Run the application - All instances are production instances
    print("🚀 Running in Production Mode (using Flask)")
    app.run(
        host=HOST,
        port=PORT,
        debug=False,  # Always False in production
        threaded=True
    )
