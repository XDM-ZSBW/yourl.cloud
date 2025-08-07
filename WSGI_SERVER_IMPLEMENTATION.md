# WSGI Server Implementation

**Production-ready WSGI server integration for Yourl Cloud Inc. API Server**

This document describes the implementation of production WSGI server support using Gunicorn for the Yourl Cloud Inc. API Server.

## 🎯 Overview

**All instances deploy as production instances** - the tester decides whether they're using it for personal or work purposes:

- **All Deployments**: Gunicorn WSGI server (production-ready)
- **Usage Context**: Determined by the tester (personal vs work)
- **Consistent Environment**: Same production configuration across all deployments

## 📁 New Files

### Core WSGI Files

1. **`wsgi.py`** - WSGI entry point for production servers
   - Imports the Flask app from `app.py`
   - Serves as the application object for WSGI servers
   - Minimal and focused on production deployment

2. **`gunicorn.conf.py`** - Gunicorn configuration
   - Optimized settings for production deployment
   - Worker process configuration based on CPU cores
   - Logging and security settings
   - Custom hooks for monitoring and debugging

3. **`start.py`** - Production startup script
   - Handles production deployment for all instances
   - Uses Gunicorn WSGI server
   - Fallback to Flask if Gunicorn unavailable
   - User-friendly startup messages

## 🔧 Configuration

### Environment Variables

- `PORT`: Port number (default: 8080)
- `FLASK_DEBUG`: Debug mode (default: False - always False in production)

### Production Mode

**All instances are production instances** - no environment detection needed:

```python
# Production mode detection - All instances deploy as production instances
PRODUCTION = True  # Always production for all deployments
```

### Gunicorn Configuration

Key settings in `gunicorn.conf.py`:

```python
# Worker processes (CPU cores * 2 + 1)
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class and connections
worker_class = "sync"
worker_connections = 1000

# Request limits and timeouts
max_requests = 1000
max_requests_jitter = 50
timeout = 30

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
```

## 🚀 Usage

### All Deployments (Production Mode)

```bash
# Using Gunicorn directly
gunicorn --config gunicorn.conf.py wsgi:app

# Using the startup script (recommended)
python start.py

# Direct execution (fallback)
python app.py
```

### Docker Deployment

The Dockerfile automatically uses Gunicorn for all deployments:

```dockerfile
# Run the application with Gunicorn (all instances are production)
CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:app"]
```

## 📊 Monitoring

### Health Check Endpoint

The `/health` endpoint includes WSGI server information:

```json
{
  "status": "healthy",
  "timestamp": "2025-08-06T12:00:00.000000",
  "service": "url-api",
  "version": "1.0.0",
  "friends_family_guard": true,
  "cloud_run_support": true,
  "wsgi_server": "gunicorn",
  "production_mode": true,
  "port": 8080
}
```

### Status Endpoint

The `/status` endpoint includes production mode information:

```json
{
  "service": "URL API with Visual Inspection",
  "version": "1.0.0",
  "status": "running",
  "port": 8080,
  "host": "0.0.0.0",
  "timestamp": "2025-08-06T12:00:00.000000",
  "session_id": "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49",
  "organization": "Yourl Cloud Inc.",
  "friends_family_guard": true,
  "visual_inspection": {
    "pc_allowed": true,
    "phone_allowed": true,
    "watch_blocked": true,
    "tablet_allowed": true
  },
  "cloud_run_support": true,
  "demo_mode": true,
  "wsgi_server": "gunicorn",
  "production_mode": true
}
```

## 🔄 Deployment Model

### All Instances Are Production Instances

- **Consistent Environment**: Same production configuration across all deployments
- **Tester Decision**: User decides whether it's for personal or work use
- **No Environment Detection**: Always production mode
- **WSGI Server**: Gunicorn for all deployments

### Local Testing

1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Test production deployment**:
   ```bash
   python start.py
   ```

3. **Verify WSGI server**:
   ```bash
   curl http://localhost:8080/health
   ```

### Cloud Deployment

1. **Build Docker image**:
   ```bash
   docker build -t yourl-cloud .
   ```

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy yourl-cloud \
     --image yourl-cloud \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8080
   ```

## 🛡️ Security Considerations

### Production Settings

- **Debug mode disabled** for all deployments
- **Worker process isolation** with Gunicorn
- **Request limits** to prevent abuse
- **Timeout settings** for resource management
- **Logging** for monitoring and debugging

### Environment Variables

- **PORT**: Automatically handled by Cloud Run
- **FLASK_DEBUG**: Always `False` (all instances are production)

## 📈 Performance

### Gunicorn Benefits

- **Multiple worker processes** for better concurrency
- **Process isolation** for stability
- **Resource management** with request limits
- **Production-grade logging** and monitoring
- **Automatic worker restart** for memory management

### Optimization

- **Worker count**: CPU cores * 2 + 1
- **Max requests**: 1000 per worker (prevents memory leaks)
- **Timeout**: 30 seconds (prevents hanging requests)
- **Keepalive**: 2 seconds (optimized for Cloud Run)

## 🔍 Troubleshooting

### Common Issues

1. **Gunicorn not found**:
   ```bash
   pip install gunicorn
   ```

2. **Port already in use**:
   ```bash
   # Check what's using the port
   lsof -i :8080
   
   # Kill the process
   kill -9 <PID>
   ```

3. **Permission denied**:
   ```bash
   # Make sure the script is executable
   chmod +x start.py
   ```

### Logs

- **Access logs**: Standard output (stdout)
- **Error logs**: Standard error (stderr)
- **Application logs**: Flask logging configuration

## 📚 References

- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Flask WSGI Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)

---

**Author**: Yourl Cloud Inc.  
**Environment**: Production (All instances)  
**WSGI Server**: Gunicorn  
**Deployment Model**: All instances are production instances  
**Last Updated**: 2025-08-06
