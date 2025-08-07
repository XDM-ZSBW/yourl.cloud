#!/usr/bin/env python3
"""
WSGI entry point for Cloud Run domain mapping compatibility
==========================================================

This file serves as the WSGI application entry point for Cloud Run deployments
with domain mapping support. It imports the Flask app from app.py and makes it
available to WSGI servers like Gunicorn and Waitress.

Author: Yourl Cloud Inc.
Environment: Production
WSGI Server: Gunicorn (Unix) / Waitress (Windows)
Domain Mapping: Compatible
Cloud Run Region: us-west1
"""

import os
import sys
from app import app, CLOUD_RUN_CONFIG

# Configure environment for Cloud Run domain mapping
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('PORT', '8080')

# Ensure the app is configured for Cloud Run
if __name__ == "__main__":
    # This allows running the WSGI file directly for testing
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
