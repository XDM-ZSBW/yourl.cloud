#!/usr/bin/env python3
"""
Gunicorn configuration for production deployment
===============================================

This file contains the configuration settings for Gunicorn WSGI server
optimized for production deployment on Google Cloud Run.

Author: Yourl Cloud Inc.
Environment: Production
WSGI Server: Gunicorn
"""

import os
import multiprocessing

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "yourl-cloud-api"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (not needed for Cloud Run as it handles HTTPS)
keyfile = None
certfile = None

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Development settings (override in production)
reload = False
reload_engine = "auto"
reload_extra_files = []
spew = False

# Server hooks
def on_starting(server):
    server.log.info("🚀 Starting Yourl Cloud Inc. API Server with Gunicorn")

def on_reload(server):
    server.log.info("🔄 Reloading Yourl Cloud Inc. API Server")

def worker_int(worker):
    worker.log.info("👷 Worker received INT or QUIT signal")

def pre_fork(server, worker):
    server.log.info("🔧 Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    server.log.info("✅ Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    worker.log.info("🎯 Worker initialized (pid: %s)", worker.pid)

def worker_abort(worker):
    worker.log.info("⚠️ Worker aborted (pid: %s)", worker.pid)
