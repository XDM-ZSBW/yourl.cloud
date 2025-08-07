#!/usr/bin/env python3
"""
Startup script for Yourl Cloud Inc. API Server
============================================

This script handles production startup mode for all deployments.
All instances deploy as production instances - the tester decides
whether they're using it for personal or work purposes.

Author: Yourl Cloud Inc.
Environment: Production (All instances)
WSGI Server: Gunicorn
"""

import os
import sys
import subprocess
from app import app, PRODUCTION, HOST, PORT, DEBUG

def start_production():
    """Start the application in production mode using Gunicorn."""
    print("🚀 Starting in Production Mode (Gunicorn WSGI server)")
    print(f"📍 Host: {HOST}")
    print(f"🔌 Port: {PORT}")
    print("🏭 Production: True (All instances are production instances)")
    print("=" * 50)
    
    # Use Gunicorn with our configuration
    cmd = [
        "gunicorn",
        "--config", "gunicorn.conf.py",
        "wsgi:app"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Gunicorn: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Gunicorn not found. Please install it with: pip install gunicorn")
        print("🔄 Falling back to Flask development server...")
        app.run(
            host=HOST,
            port=PORT,
            debug=False,  # Always False in production
            threaded=True
        )

def main():
    """Main entry point - all instances are production instances."""
    print("🚀 Yourl Cloud Inc. API Server Startup")
    print("🏭 All instances deploy as production instances")
    print("👤 Tester decides: Personal use or Work use")
    print("=" * 50)
    
    # All instances are production instances
    start_production()

if __name__ == "__main__":
    main()
