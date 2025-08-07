# Cloud Run Domain Mapping Compatibility Guide

## Overview

This guide provides step-by-step instructions for deploying your Flask application to Google Cloud Run with custom domain mapping support, specifically optimized for the `us-west1` region.

## Prerequisites

1. **Google Cloud Project** with billing enabled
2. **gcloud CLI** installed and configured
3. **Docker** installed (for local testing)
4. **Domain name** registered and ready for mapping

## Key Features for Domain Mapping

### ✅ Implemented Features

- **X-Forwarded Headers Support**: Proper handling of `X-Forwarded-For`, `X-Forwarded-Host`, `X-Forwarded-Proto`
- **Health Check Endpoint**: `/health` endpoint for Cloud Run health checks
- **CORS Compatibility**: Configured for domain mapping cross-origin requests
- **HTTPS Support**: Automatic HTTPS detection and protocol handling
- **Proxy Trust**: Configured to trust Cloud Run's proxy headers
- **Domain Detection**: Real-time domain and protocol detection

### 🔧 Configuration

```python
# Cloud Run Domain Mapping Configuration
CLOUD_RUN_CONFIG = {
    "domain_mapping_enabled": True,
    "region": "us-west1",  # Default region for domain mappings
    "trust_proxy": True,  # Trust X-Forwarded headers from Cloud Run proxy
    "cors_enabled": True,  # Enable CORS for domain mapping compatibility
    "health_check_path": "/health",  # Health check endpoint for Cloud Run
    "readiness_check_path": "/health"  # Readiness check endpoint
}
```

## Deployment Steps

### 1. Build and Deploy to Cloud Run

```bash
# Set your project ID
export PROJECT_ID="your-project-id"

# Build the Docker image
gcloud builds submit --tag gcr.io/$PROJECT_ID/yourl-cloud .

# Deploy to Cloud Run
gcloud run deploy yourl-cloud \
  --image gcr.io/$PROJECT_ID/yourl-cloud:latest \
  --region=us-west1 \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080 \
  --memory=512Mi \
  --cpu=1 \
  --max-instances=10 \
  --timeout=300 \
  --concurrency=80
```

### 2. Map Custom Domain

```bash
# Map your custom domain
gcloud run domain-mappings create \
  --service yourl-cloud \
  --domain yourl.cloud \
  --region us-west1 \
  --platform managed
```

### 3. Verify Domain Mapping

```bash
# Check domain mapping status
gcloud run domain-mappings describe \
  --domain yourl.cloud \
  --region us-west1 \
  --platform managed
```

## Environment Variables

### Required Environment Variables

```bash
# Cloud Run automatically sets these
PORT=8080                    # Port for the application
FLASK_ENV=production         # Production environment
FLASK_APP=app.py            # Flask application entry point
```

### Optional Environment Variables

```bash
# Custom configuration
FLASK_DEBUG=False           # Debug mode (should be False for production)
CLOUD_RUN_REGION=us-west1   # Cloud Run region
```

## Health Checks

### Health Check Endpoint

The application provides a health check endpoint at `/health` that returns:

```json
{
  "status": "healthy",
  "timestamp": "2025-08-07T10:57:57.123456Z",
  "service": "url-api",
  "version": "1.0.0",
  "cloud_run_support": true,
  "domain_mapping": {
    "enabled": true,
    "region": "us-west1",
    "health_check_path": "/health"
  },
  "wsgi_server": "gunicorn",
  "production_mode": true,
  "deployment_model": "all_instances_production",
  "port": 8080,
  "host": "yourl.cloud",
  "protocol": "https"
}
```

### Health Check Configuration

```yaml
# Cloud Run health check configuration
healthCheck:
  path: /health
  port: 8080
  timeoutSeconds: 10
  initialDelaySeconds: 5
  periodSeconds: 30
  failureThreshold: 3
  successThreshold: 1
```

## Domain Mapping Features

### Automatic Domain Detection

The application automatically detects and displays:

- **Original Host**: From `X-Forwarded-Host` header
- **Original Protocol**: From `X-Forwarded-Proto` header (always HTTPS for Cloud Run)
- **Client IP**: From `X-Forwarded-For` header

### Visual Inspection with Domain Info

The visual inspection interface now includes a Cloud Run information card showing:

- Domain name
- Protocol (HTTPS)
- Domain mapping status

## Security Considerations

### ✅ Security Features

- **HTTPS Only**: Cloud Run always serves HTTPS
- **X-Forwarded Headers**: Properly validated and sanitized
- **CORS Configuration**: Configured for domain mapping compatibility
- **Health Checks**: Secure health check endpoint
- **Error Handling**: Proper error responses with domain information

### 🔒 Security Best Practices

1. **Never trust user input**: All headers are validated
2. **Use HTTPS**: Cloud Run automatically handles SSL/TLS
3. **Health checks**: Use the dedicated `/health` endpoint
4. **Error logging**: Proper error logging without exposing sensitive data

## Troubleshooting

### Common Issues

#### 1. Domain Mapping Not Working

```bash
# Check domain mapping status
gcloud run domain-mappings list --region=us-west1

# Verify DNS configuration
dig yourl.cloud
```

#### 2. Health Check Failures

```bash
# Test health endpoint locally
curl -f http://localhost:8080/health

# Check Cloud Run logs
gcloud logs read --service=yourl-cloud --limit=50
```

#### 3. X-Forwarded Headers Not Working

```bash
# Test with curl
curl -H "X-Forwarded-Host: yourl.cloud" \
     -H "X-Forwarded-Proto: https" \
     -H "X-Forwarded-For: 1.2.3.4" \
     http://localhost:8080/api
```

### Debug Mode

For debugging, you can enable debug mode:

```bash
# Set debug environment variable
export FLASK_DEBUG=true

# Run locally with debug
python app.py
```

## Monitoring and Logging

### Cloud Run Logs

```bash
# View real-time logs
gcloud logs tail --service=yourl-cloud --region=us-west1

# View specific log entries
gcloud logs read --service=yourl-cloud --limit=100
```

### Application Metrics

The application provides metrics at:

- `/health` - Health check and basic metrics
- `/status` - Detailed service status
- `/guard` - Friends and Family Guard status

## Performance Optimization

### Gunicorn Configuration

```python
# Optimized for Cloud Run
CMD ["gunicorn", 
     "--bind", "0.0.0.0:8080", 
     "--workers", "4", 
     "--timeout", "120", 
     "--keep-alive", "2", 
     "--max-requests", "1000",
     "--max-requests-jitter", "100",
     "wsgi:app"]
```

### Resource Allocation

```bash
# Recommended Cloud Run configuration
--memory=512Mi      # Adequate for most workloads
--cpu=1            # Single CPU for cost optimization
--max-instances=10 # Scale up to 10 instances
--concurrency=80   # Handle 80 concurrent requests per instance
```

## Cost Optimization

### Resource Recommendations

- **Memory**: 512Mi (sufficient for Flask + Gunicorn)
- **CPU**: 1 (cost-effective for most workloads)
- **Max Instances**: 10 (prevents runaway scaling)
- **Concurrency**: 80 (optimal for Gunicorn workers)

### Scaling Configuration

```bash
# Auto-scaling configuration
gcloud run services update yourl-cloud \
  --region=us-west1 \
  --min-instances=0 \
  --max-instances=10 \
  --concurrency=80 \
  --cpu-throttling
```

## Support and Maintenance

### Regular Maintenance

1. **Security Updates**: Regularly update dependencies
2. **Health Monitoring**: Monitor `/health` endpoint
3. **Log Analysis**: Review Cloud Run logs regularly
4. **Performance Monitoring**: Monitor response times and errors

### Contact Information

- **Organization**: Yourl Cloud Inc.
- **Support**: Check GitHub issues for support
- **Documentation**: This guide and README.md

## Conclusion

Your Flask application is now fully compatible with Google Cloud Run domain mappings. The implementation includes:

- ✅ Full domain mapping support
- ✅ X-Forwarded headers handling
- ✅ Health check compatibility
- ✅ Security best practices
- ✅ Performance optimization
- ✅ Comprehensive monitoring

For additional support or questions, refer to the [Google Cloud Run documentation](https://cloud.google.com/run/docs/mapping-custom-domains) or create an issue in the GitHub repository.
