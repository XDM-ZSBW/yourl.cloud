# Yourl.Cloud - URL API Server with Visual Inspection

**Last Updated**: 2025-08-07T13:16:32.276259
**Session ID**: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
**Organization**: Yourl Cloud Inc.
**Branch**: main
**Commit**: a2fc53f9
**Commit Date**: 2025-08-07 06:16:31 -0700

## 🎯 Project Overview

Yourl.Cloud is a production-ready Python Flask API that returns the request URL with advanced visual inspection capabilities. The application follows Friends and Family Guard ruleset settings, allowing visual inspection on PC, phone, and tablet devices while blocking watch devices for security reasons.

**Key Innovation**: Full Google Cloud Run domain mapping compatibility with automatic X-Forwarded header support.

## ✅ Current Features

- 🌐 **Cloud Run Domain Mapping**: Full compatibility with custom domains
- 🛡️ **Friends and Family Guard**: Security ruleset compliance
- 👁️ **Visual Inspection**: Modern web interface for allowed devices
- 📱 **Device Detection**: Automatic detection of PC, phone, tablet, watch
- 🏥 **Health Checks**: Cloud Run compatible health endpoints
- 🔗 **X-Forwarded Headers**: Proper proxy header handling
- 🚀 **WSGI Server**: Production-ready Gunicorn/Waitress support
- 🌍 **Domain Mapping**: Custom domain support (yourl.cloud)

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/XDM-ZSBW/yourl.cloud.git
cd yourl.cloud

# Install dependencies
pip install -r requirements.txt

# Run application (All instances are production instances)
python app.py
```

### Cloud Run Deployment

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/$PROJECT_ID/yourl-cloud .
gcloud run deploy yourl-cloud \
  --image gcr.io/$PROJECT_ID/yourl-cloud:latest \
  --region=us-west1 \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080

# Map custom domain
gcloud run domain-mappings create \
  --service yourl-cloud \
  --domain yourl.cloud \
  --region us-west1 \
  --platform managed
```

## 📱 Device Support

| Device Type | Visual Inspection | Status | Security |
|-------------|-------------------|--------|----------|
| PC          | ✅ Allowed        | Full access | Friends & Family Guard |
| Phone       | ✅ Allowed        | Full access | Friends & Family Guard |
| Tablet      | ✅ Allowed        | Full access | Friends & Family Guard |
| Watch       | ❌ Blocked        | Security rule | Friends & Family Guard |

## 🔌 API Endpoints

- `GET /` - Main endpoint (JSON or HTML with domain info)
- `GET /health` - Health check with Cloud Run compatibility
- `GET /status` - Service status with domain mapping info
- `GET /guard` - Friends and Family Guard status
- `GET /api` - Visual inspection interface

## 🛡️ Friends and Family Guard

The application implements a comprehensive security ruleset that:
- ✅ Allows visual inspection on PC, phone, and tablet devices
- ❌ Blocks visual inspection on watch devices for security
- 🔍 Provides transparent status reporting
- 🎯 Ensures appropriate access control
- 🌐 Supports domain mapping with X-Forwarded headers

## 🌍 Domain Mapping Features

### ✅ Implemented Features
- **X-Forwarded Headers Support**: Proper handling of `X-Forwarded-For`, `X-Forwarded-Host`, `X-Forwarded-Proto`
- **Health Check Endpoint**: `/health` endpoint for Cloud Run health checks
- **CORS Compatibility**: Configured for domain mapping cross-origin requests
- **HTTPS Support**: Automatic HTTPS detection and protocol handling
- **Proxy Trust**: Configured to trust Cloud Run's proxy headers
- **Domain Detection**: Real-time domain and protocol detection

### 🔧 Configuration
```python
CLOUD_RUN_CONFIG = {
    "domain_mapping_enabled": True,
    "region": "us-west1",
    "trust_proxy": True,
    "cors_enabled": True,
    "health_check_path": "/health",
    "readiness_check_path": "/health"
}
```

## 📅 Timeline

### Recent Development
- **2025-08-07**: Current - Cloud Run Domain Mapping Implementation

### Key Milestones
- **2025-08-07**: Cloud Run Domain Mapping Implementation
- **2025-08-07**: X-Forwarded Headers Support
- **2025-08-07**: Health Check Compatibility
- **2025-08-07**: Production WSGI Server Integration
- **2025-08-06**: Friends and Family Guard Implementation
- **2025-08-06**: Visual Inspection Interface
- **2025-08-06**: Device Detection System

## 🔮 Future Roadmap

### Planned Features
- 🔐 **Enhanced Authentication**: OAuth 2.0 integration
- 📊 **Analytics Dashboard**: Usage metrics and monitoring
- 🔄 **Auto-scaling**: Advanced Cloud Run scaling policies
- 🛡️ **Security Scanning**: Automated vulnerability detection
- 🌐 **Multi-region**: Global deployment support

### Development Priorities
1. **Security Hardening**: Advanced security features
2. **Performance Optimization**: Enhanced caching and CDN
3. **Monitoring**: Comprehensive logging and alerting
4. **Documentation**: Enhanced guides and tutorials

## 🏗️ Architecture

### Current Stack
- **Backend**: Python Flask 3.0.2
- **WSGI Server**: Gunicorn (Unix) / Waitress (Windows)
- **Deployment**: Google Cloud Run
- **Domain**: yourl.cloud (custom domain mapping)
- **Security**: Friends and Family Guard ruleset

### Production Features
- ✅ **All instances are production instances**
- ✅ **Automatic health checks**
- ✅ **Domain mapping compatibility**
- ✅ **X-Forwarded header support**
- ✅ **HTTPS enforcement**
- ✅ **Error handling and logging**

## 📚 Documentation

### Key Documents
- **[README.md](https://github.com/XDM-ZSBW/yourl.cloud/blob/main/README.md)**: Main project documentation
- **[CLOUD_RUN_DOMAIN_MAPPING.md](https://github.com/XDM-ZSBW/yourl.cloud/blob/main/CLOUD_RUN_DOMAIN_MAPPING.md)**: Domain mapping guide
- **[STATUS.md](https://github.com/XDM-ZSBW/yourl.cloud/blob/main/STATUS.md)**: Current project status
- **[SECURITY.md](https://github.com/XDM-ZSBW/yourl.cloud/blob/main/SECURITY.md)**: Security policy

## 🎯 Context

This project evolved from a simple URL API to a comprehensive cloud-native application with:
- **Visual inspection capabilities** for modern web interfaces
- **Security-first approach** with Friends and Family Guard
- **Cloud Run compatibility** for scalable deployment
- **Domain mapping support** for custom domains
- **Production-ready architecture** with WSGI servers

The application serves as both a testing/development tool and a production service, providing programmatic access (JSON) and visual inspection (HTML) based on device capabilities and security rules.

## 🔗 Source of Truth

**yourl.cloud** is always the source of truth for latest information. This wiki is automatically updated from the main repository after each commit.

### Wiki Update Process
1. **Automatic Updates**: Wiki updates after each commit
2. **Linear Progression**: README.md maintains current state
3. **Past/Present/Future**: Wiki includes historical context and future roadmap
4. **Real-time Sync**: Wiki reflects current repository state

---

*Generated on 2025-08-07T13:16:32.276259 | Branch: main | Commit: a2fc53f9*
