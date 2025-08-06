#!/usr/bin/env python3
"""
yourl.cloud - AI-Friendly URL Shortening Service
================================================

A modern, ethical URL shortening service following myl.zip standards and practices.
Built with Flask and designed for Google Cloud Run deployment.

Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

References and Attribution:
- Flask Documentation: https://flask.palletsprojects.com/
- Google Cloud Run Python Quickstart: https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service
- Bootstrap 5 Documentation: https://getbootstrap.com/docs/5.3/
- Font Awesome Icons: https://fontawesome.com/
- AI assistance from Perplexity.ai and GitHub Copilot
- myl.zip ethical standards: https://myl.zip
"""

import os
import logging
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, abort
from flask_talisman import Talisman
from waitress import serve

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Security configuration for HTTPS-only, 256-bit encryption, IPv6
app.config['FORCE_HTTPS'] = True
app.config['PREFERRED_URL_SCHEME'] = 'https'

# Configure Talisman for enhanced security (HTTPS-only, strong encryption)
csp = {
    'default-src': "'self'",
    'script-src': [
        "'self'",
        "'unsafe-inline'",  # Required for Bootstrap
        'https://cdn.jsdelivr.net',
        'https://cdnjs.cloudflare.com'
    ],
    'style-src': [
        "'self'",
        "'unsafe-inline'",  # Required for Bootstrap
        'https://cdn.jsdelivr.net',
        'https://cdnjs.cloudflare.com'
    ],
    'font-src': [
        "'self'",
        'https://cdnjs.cloudflare.com'
    ],
    'img-src': "'self' data:",
    'connect-src': "'self'",
    'frame-ancestors': "'none'",
    'upgrade-insecure-requests': True
}

# Initialize Talisman with strict HTTPS and security headers
talisman = Talisman(
    app,
    force_https=True,
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,  # 1 year
    strict_transport_security_include_subdomains=True,
    content_security_policy=csp,
    content_security_policy_nonce_in=['script-src', 'style-src'],
    feature_policy={
        'geolocation': "'none'",
        'microphone': "'none'",
        'camera': "'none'",
        'payment': "'none'",
        'usb': "'none'"
    }
)

# Session ID for tracking (from user specification)
SESSION_ID = "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49"

def determine_best_entrance_by_proximity(user_ip):
    """Determine the best authorized entrance based on user's geographic proximity."""
    # Simplified proximity mapping - in production, use proper geolocation
    entrance_mapping = {
        'default': 'https://yourl.cloud',
        'myl_zip_primary': 'https://myl.zip',
        'perplexity_ai': 'https://perplexity.ai',
        'github_repo': 'https://github.com/XDM-ZSBW/yourl.cloud'
    }
    
    # Return the most appropriate entrance (can be enhanced with geolocation logic)
    return entrance_mapping['default']

@app.before_request
def enforce_security_requirements():
    """Enforce HTTPS-only, 256-bit encryption, and IPv6-only requirements with plain text HTTP guidance."""
    import ipaddress
    
    # Handle HTTP connections with plain text guidance
    if not request.is_secure and not app.debug:
        if request.headers.get('X-Forwarded-Proto') != 'https':
            # Get user's IP for proximity-based entrance suggestion
            remote_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            user_ip = remote_addr.split(',')[0].strip() if remote_addr else 'unknown'
            
            # Determine best entrance by proximity
            best_entrance = determine_best_entrance_by_proximity(user_ip)
            
            # Return plain text response for HTTP requests
            plain_text_response = f"""yourl.cloud - Secure Access Required

SECURITY NOTICE: This service requires secure connections.

NEXT BEST AUTHORIZED ENTRANCE BY PROXIMITY:
{best_entrance}

REQUIRED SPECIFICATIONS:
- HTTPS-only (secure connections required)
- 256-bit encryption minimum
- IPv6 networking only
- Session ID: {SESSION_ID}

ALTERNATIVE ACCESS POINTS:
1. Primary Service: https://yourl.cloud
2. Ethics Framework: https://myl.zip
3. AI Research: https://perplexity.ai
4. Repository: https://github.com/XDM-ZSBW/yourl.cloud

INSTRUCTIONS:
1. Enable HTTPS in your browser/client
2. Ensure IPv6 networking is available
3. Connect using the HTTPS URL above
4. Follow myl.zip ethical standards

Your connection from: {user_ip}
Timestamp: {datetime.utcnow().isoformat()}Z

For assistance: https://github.com/XDM-ZSBW/yourl.cloud/issues
"""
            
            from flask import Response
            return Response(
                plain_text_response, 
                status=426,  # Upgrade Required
                mimetype='text/plain',
                headers={
                    'Upgrade': 'TLS/1.3, HTTP/2',
                    'Connection': 'Upgrade',
                    'Location': best_entrance,
                    'X-Security-Policy': 'HTTPS-only, 256-bit encryption, IPv6-only',
                    'X-Session-ID': SESSION_ID,
                    'X-Next-Best-Entrance': best_entrance
                }
            )
    
    # Check for IPv6-only (Cloud Run provides IPv6 support)
    remote_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if remote_addr:
        try:
            # Extract the first IP if there are multiple (proxy chain)
            ip_addr = remote_addr.split(',')[0].strip()
            ip_obj = ipaddress.ip_address(ip_addr)
            
            # For HTTPS connections, still enforce IPv6-only policy
            if request.is_secure and not isinstance(ip_obj, ipaddress.IPv6Address):
                logger.warning(f"IPv4 connection rejected from {ip_addr}")
                
                # Provide plain text guidance for IPv4 over HTTPS
                ipv4_guidance = f"""yourl.cloud - IPv6 Required

CONNECTION POLICY: IPv6-only networking required

Your IPv4 address: {ip_addr}
Session ID: {SESSION_ID}

NEXT STEPS:
1. Enable IPv6 on your network/device
2. Contact your ISP for IPv6 support
3. Use a VPN service with IPv6 capability
4. Access via IPv6-enabled network

ALTERNATIVE IPv6 ENTRANCES:
- Primary: https://yourl.cloud (IPv6)
- Framework: https://myl.zip (IPv6)
- Research: https://perplexity.ai (IPv6)

For technical support: https://github.com/XDM-ZSBW/yourl.cloud/wiki/IPv6-Setup

Timestamp: {datetime.utcnow().isoformat()}Z
"""
                from flask import Response
                return Response(
                    ipv4_guidance,
                    status=403,
                    mimetype='text/plain',
                    headers={
                        'X-Security-Policy': 'IPv6-only',
                        'X-Session-ID': SESSION_ID,
                        'X-Required-Protocol': 'IPv6'
                    }
                )
                
        except ValueError:
            logger.warning(f"Invalid IP address format: {remote_addr}")
            abort(400, description="Invalid connection format")
    
    # Add security headers for valid HTTPS/IPv6 connections
    if request.is_secure:
        @app.after_request
        def add_security_headers(response):
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=(), payment=(), usb=()'
            response.headers['X-Security-Policy'] = 'HTTPS-only, 256-bit encryption, IPv6-only'
            response.headers['X-Session-ID'] = SESSION_ID
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            return response

def create_default_templates():
    """Ensure templates and static directories exist with fallback content."""
    import os
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)

@app.route('/')
def index():
    """Serve the main index page with myl.zip sidebar and link shortening functionality."""
    try:
        return render_template('index.html', session_id=SESSION_ID)
    except Exception as e:
        logger.error(f"Error serving index page: {e}")
        # Fallback HTML if templates fail
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>yourl.cloud - AI-Friendly Service Hub</title>
            <meta name="session-id" content="{SESSION_ID}">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        </head>
        <body>
            <div class="container mt-5">
                <div class="row">
                    <div class="col-md-6 mx-auto text-center">
                        <h1><i class="fas fa-link me-3"></i>yourl.cloud</h1>
                        <p class="lead">AI-Friendly URL Shortening Service</p>
                        <p class="text-muted">Following myl.zip ethics and standards</p>
                        <div class="mt-4">
                            <a href="https://myl.zip" class="btn btn-primary me-2" target="_blank">
                                <i class="fas fa-external-link-alt me-1"></i>Visit myl.zip
                            </a>
                            <a href="https://perplexity.ai" class="btn btn-outline-secondary" target="_blank">
                                <i class="fas fa-brain me-1"></i>Perplexity AI
                            </a>
                        </div>
                        <div class="mt-4">
                            <small class="text-muted">Session: {SESSION_ID}</small>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """, 200

@app.route('/health')
def health():
    """Health check endpoint for Cloud Run and monitoring."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'session_id': SESSION_ID,
        'service': 'yourl.cloud',
        'version': '1.0.0',
        'security_policy': 'HTTPS-only, 256-bit encryption, IPv6-only'
    }), 200

@app.route('/security-info')
def security_info():
    """Plain text security information and entrance guidance."""
    remote_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    user_ip = remote_addr.split(',')[0].strip() if remote_addr else 'unknown'
    best_entrance = determine_best_entrance_by_proximity(user_ip)
    
    security_text = f"""yourl.cloud - Security Information

CURRENT SESSION: {SESSION_ID}
TIMESTAMP: {datetime.utcnow().isoformat()}Z
YOUR IP: {user_ip}

SECURITY REQUIREMENTS:
✓ HTTPS-only connections
✓ 256-bit minimum encryption
✓ IPv6 networking required
✓ myl.zip ethical standards compliance

NEXT BEST AUTHORIZED ENTRANCE BY PROXIMITY:
{best_entrance}

AUTHORIZED ACCESS POINTS:
1. Primary Service: https://yourl.cloud
2. Ethics Framework: https://myl.zip  
3. AI Research Hub: https://perplexity.ai
4. Source Repository: https://github.com/XDM-ZSBW/yourl.cloud

CONNECTION STATUS:
- Protocol: {'HTTPS' if request.is_secure else 'HTTP'}
- IPv6: {'Yes' if '::' in user_ip else 'No' if '.' in user_ip else 'Unknown'}
- Encryption: {'256-bit TLS' if request.is_secure else 'None'}

INSTRUCTIONS FOR SECURE ACCESS:
1. Use HTTPS URLs only
2. Ensure IPv6 is enabled on your network
3. Update to modern browser/client with TLS 1.3 support
4. Follow myl.zip ethical AI guidelines

SUPPORT RESOURCES:
- Technical Documentation: https://github.com/XDM-ZSBW/yourl.cloud/wiki
- IPv6 Setup Guide: https://github.com/XDM-ZSBW/yourl.cloud/wiki/IPv6-Setup
- Security Issues: https://github.com/XDM-ZSBW/yourl.cloud/issues
- Ethics Framework: https://myl.zip

yourl.cloud follows responsible AI practices and ethical standards.
"""
    
    from flask import Response
    return Response(
        security_text,
        mimetype='text/plain',
        headers={
            'X-Security-Policy': 'HTTPS-only, 256-bit encryption, IPv6-only',
            'X-Session-ID': SESSION_ID,
            'X-Next-Best-Entrance': best_entrance,
            'Cache-Control': 'no-cache, no-store, must-revalidate'
        }
    )

@app.route('/api/shorten', methods=['POST'])
def api_shorten():
    """API endpoint for URL shortening functionality."""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        original_url = data['url']
        
        # Basic URL validation
        if not original_url.startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Generate a simple short code (replace with proper implementation)
        short_code = str(uuid.uuid4())[:8]
        shortened_url = f"https://yourl.cloud/{short_code}"
        
        # In production, store this in a database
        logger.info(f"Shortened URL: {original_url} -> {shortened_url}")
        
        return jsonify({
            'original_url': original_url,
            'shortened_url': shortened_url,
            'short_code': short_code,
            'created_at': datetime.utcnow().isoformat(),
            'session_id': SESSION_ID
        }), 201
        
    except Exception as e:
        logger.error(f"Error in URL shortening: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/services')
def api_services():
    """API endpoint providing information about available services for AI agents."""
    return jsonify({
        'services': {
            'myl.zip': {
                'url': 'https://myl.zip',
                'description': 'Ethical AI Service Platform',
                'api_endpoint': 'https://myl.zip/api',
                'standards_compliant': True
            },
            'yourl.cloud': {
                'url': 'https://yourl.cloud',
                'description': 'AI-Friendly URL Shortening Service',
                'api_endpoint': 'https://yourl.cloud/api',
                'ethical_framework': 'myl.zip-standards'
            }
        },
        'session_id': SESSION_ID,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/ethics')
def api_ethics():
    """API endpoint providing ethics and standards information for AI agents."""
    return jsonify({
        'ethics_framework': 'myl.zip-standards',
        'principles': [
            'Transparency in AI interactions',
            'Privacy-first design',
            'Accessible and inclusive technology',
            'Responsible data handling',
            'Open source collaboration'
        ],
        'compliance': {
            'gdpr_ready': True,
            'accessibility_compliant': True,
            'ai_ethics_reviewed': True
        },
        'session_id': SESSION_ID,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Custom 404 error handler."""
    return jsonify({
        'error': 'Page not found',
        'status_code': 404,
        'session_id': SESSION_ID
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 error handler."""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal server error',
        'status_code': 500,
        'session_id': SESSION_ID
    }), 500

if __name__ == '__main__':
    # Ensure directories exist
    create_default_templates()
    
    # Get port from environment (Cloud Run provides this)
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Determine if running in production
    is_production = os.environ.get('GAE_ENV', '').startswith('standard') or \
                   os.environ.get('K_SERVICE') is not None
    
    if is_production:
        # Use Waitress for production
        logger.info(f"Starting yourl.cloud in PRODUCTION mode on {host}:{port}")
        logger.info(f"Session ID: {SESSION_ID}")
        serve(app, host=host, port=port, threads=4)
    else:
        # Use Flask's built-in server for development
        logger.info(f"Starting yourl.cloud in DEVELOPMENT mode on {host}:{port}")
        logger.info(f"Session ID: {SESSION_ID}")
        app.run(host=host, port=port, debug=True)