#!/usr/bin/env python3
"""
WSGI entry point for production deployment with Gunicorn
========================================================

This file serves as the WSGI application entry point for production deployments.
It imports the Flask app from app.py and makes it available to WSGI servers like Gunicorn.

Author: Yourl Cloud Inc.
Environment: Production
WSGI Server: Gunicorn
"""

from app import app

if __name__ == "__main__":
    app.run()
