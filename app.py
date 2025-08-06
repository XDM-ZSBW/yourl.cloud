#!/usr/bin/env python3
"""
yourl.cloud - A simple HTML hosting application for Google Cloud Run
Self-configuring auto-starting Python app
"""

import os
import logging
from flask import Flask, render_template, send_from_directory
from waitress import serve

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Auto-configure from environment variables
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
    DEBUG=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true',
)

@app.route('/')
def index():
    """Serve the main index page"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving index page: {e}")
        return f"<h1>yourl.cloud</h1><p>Welcome to yourl.cloud!</p><p>Error: {e}</p>", 500

@app.route('/health')
def health_check():
    """Health check endpoint for Cloud Run"""
    return {'status': 'healthy', 'service': 'yourl.cloud'}, 200

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.errorhandler(404)
def not_found(error):
    """Custom 404 page"""
    try:
        return render_template('404.html'), 404
    except:
        return "<h1>404 - Page Not Found</h1><p>The requested page could not be found.</p>", 404

@app.errorhandler(500)
def server_error(error):
    """Custom 500 page"""
    logger.error(f"Server error: {error}")
    try:
        return render_template('500.html'), 500
    except:
        return "<h1>500 - Server Error</h1><p>An internal server error occurred.</p>", 500

def create_default_templates():
    """Create default templates if they don't exist"""
    templates_dir = 'templates'
    static_dir = 'static'
    
    # Ensure directories exist
    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(os.path.join(static_dir, 'css'), exist_ok=True)
    os.makedirs(os.path.join(static_dir, 'js'), exist_ok=True)
    
    logger.info("Template and static directories ensured")

if __name__ == '__main__':
    # Self-configure on startup
    create_default_templates()
    
    # Get port from environment variable (Cloud Run sets this)
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"Starting yourl.cloud server on {host}:{port}")
    
    if app.config['DEBUG']:
        # Development server
        app.run(host=host, port=port, debug=True)
    else:
        # Production server with Waitress
        serve(app, host=host, port=port, threads=4)