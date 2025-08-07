#!/usr/bin/env python3
"""
Simple API Server with Visual Inspection
========================================

A self-executing Python Flask application that responds with the request URL
and provides visual inspection capabilities for PC and phone devices.

Author: Yourl-Cloud Inc.
Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
Friends and Family Guard: Enabled
"""

from flask import Flask, request, jsonify, render_template_string
import socket
import os
import re
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)

# Configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 80         # Standard HTTP port
DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

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
    "organization": "Yourl-Cloud Inc."
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
    if any(keyword in ua_lower for keyword in ['tablet', 'ipad', 'kindle']):
        return 'tablet'
    
    # PC detection (default for desktop browsers)
    if any(keyword in ua_lower for keyword in ['windows', 'macintosh', 'linux', 'x11', 'desktop']):
        return 'pc'
    
    return 'unknown'

def is_visual_inspection_allowed(device_type):
    """
    Check if visual inspection is allowed for the device type.
    """
    if not FRIENDS_FAMILY_GUARD["enabled"]:
        return True
    
    rules = FRIENDS_FAMILY_GUARD["visual_inspection"]
    
    if device_type == 'watch':
        return not rules["watch_blocked"]
    elif device_type == 'pc':
        return rules["pc_allowed"]
    elif device_type == 'phone':
        return rules["phone_allowed"]
    elif device_type == 'tablet':
        return rules["tablet_allowed"]
    
    return False

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def get_request_url():
    """
    Main endpoint that returns the request URL and metadata.
    Supports visual inspection for allowed devices.
    """
    # Get the full request URL
    url = request.url
    base_url = request.base_url
    full_path = request.full_path
    
    # Get request metadata
    method = request.method
    headers = dict(request.headers)
    remote_addr = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Detect device type
    device_type = detect_device_type(user_agent)
    visual_allowed = is_visual_inspection_allowed(device_type)
    
    # Get server info
    hostname = socket.gethostname()
    timestamp = datetime.utcnow().isoformat()
    
    # Check if client wants HTML response
    accepts_html = 'text/html' in request.headers.get('Accept', '')
    
    if accepts_html and visual_allowed:
        return render_visual_inspection(url, device_type, timestamp)
    
    # Prepare JSON response
    response_data = {
        "url": url,
        "base_url": base_url,
        "full_path": full_path,
        "method": method,
        "remote_addr": remote_addr,
        "user_agent": user_agent,
        "device_type": device_type,
        "visual_inspection_allowed": visual_allowed,
        "hostname": hostname,
        "timestamp": timestamp,
        "headers": headers,
        "session_id": FRIENDS_FAMILY_GUARD["session_id"],
        "organization": FRIENDS_FAMILY_GUARD["organization"],
        "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"]
    }
    
    return jsonify(response_data)

def render_visual_inspection(url, device_type, timestamp):
    """
    Render visual inspection interface for allowed devices.
    """
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visual Inspection - URL API</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .inspection-panel {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            padding: 2rem;
            margin-bottom: 2rem;
        }
        
        .url-display {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            word-break: break-all;
            font-family: 'Courier New', monospace;
            font-size: 1.1rem;
        }
        
        .metadata-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .metadata-item {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 1rem;
        }
        
        .metadata-item h3 {
            margin-bottom: 0.5rem;
            color: #ffd700;
        }
        
        .device-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.9rem;
        }
        
        .device-pc { background: #4CAF50; }
        .device-phone { background: #2196F3; }
        .device-tablet { background: #FF9800; }
        .device-watch { background: #F44336; }
        
        .guard-status {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1rem;
        }
        
        .guard-status h3 {
            color: #ffd700;
            margin-bottom: 0.5rem;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 0.5rem;
        }
        
        .status-active { background: #4CAF50; }
        .status-inactive { background: #F44336; }
        
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .metadata-grid {
                grid-template-columns: 1fr;
            }
        }
        
        .refresh-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 1rem 2rem;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            margin-top: 1rem;
        }
        
        .refresh-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Visual Inspection</h1>
            <p>URL API Server - Friends and Family Guard Enabled</p>
        </div>
        
        <div class="inspection-panel">
            <h2>Request URL</h2>
            <div class="url-display">{{ url }}</div>
            
            <div class="metadata-grid">
                <div class="metadata-item">
                    <h3>Device Type</h3>
                    <span class="device-badge device-{{ device_type }}">{{ device_type.upper() }}</span>
                </div>
                
                <div class="metadata-item">
                    <h3>Timestamp</h3>
                    <p>{{ timestamp }}</p>
                </div>
                
                <div class="metadata-item">
                    <h3>Session ID</h3>
                    <p>{{ session_id }}</p>
                </div>
                
                <div class="metadata-item">
                    <h3>Organization</h3>
                    <p>{{ organization }}</p>
                </div>
            </div>
            
            <div class="guard-status">
                <h3>Friends and Family Guard Status</h3>
                <p>
                    <span class="status-indicator status-active"></span>
                    Visual inspection allowed for {{ device_type }} devices
                </p>
                <p>Watch devices are blocked for visual inspection per security rules.</p>
            </div>
            
            <button class="refresh-btn" onclick="location.reload()">
                🔄 Refresh Inspection
            </button>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 30 seconds for real-time inspection
        setTimeout(() => {
            location.reload();
        }, 30000);
        
        // Add keyboard shortcut for refresh (Ctrl+R or Cmd+R)
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
                e.preventDefault();
                location.reload();
            }
        });
    </script>
</body>
</html>
    """
    
    return render_template_string(html_template, 
                                url=url,
                                device_type=device_type,
                                timestamp=timestamp,
                                session_id=FRIENDS_FAMILY_GUARD["session_id"],
                                organization=FRIENDS_FAMILY_GUARD["organization"])

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "url-api",
        "version": "1.0.0",
        "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"]
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
        "visual_inspection": FRIENDS_FAMILY_GUARD["visual_inspection"]
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
    print(f"🆔 Session: {FRIENDS_FAMILY_GUARD['session_id']}")
    print(f"🏢 Organization: {FRIENDS_FAMILY_GUARD['organization']}")
    print(f"🛡️ Friends and Family Guard: {'Enabled' if FRIENDS_FAMILY_GUARD['enabled'] else 'Disabled'}")
    print(f"👁️ Visual Inspection: PC/Phone/Tablet allowed, Watch blocked")
    print(f"🌐 Access: http://{HOST}:{PORT}")
    print("=" * 60)
    
    # Run the application
    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG,
        threaded=True
    )
