# URL API Server with Visual Inspection

**Last Updated**: 2025-08-06T12:00:00.000000
**Session ID**: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
**Organization**: Yourl Cloud Inc.

## Project Overview

This is a simple Python Flask API that returns the request URL with visual inspection capabilities. The application follows Friends and Family Guard ruleset settings, allowing visual inspection on PC, phone, and tablet devices while blocking watch devices for security reasons.

## Current Features

- ✅ **URL API**: Returns request URL and metadata in JSON format
- ✅ **Visual Inspection**: Modern web interface for allowed devices
- ✅ **Device Detection**: Automatic detection of PC, phone, tablet, watch
- ✅ **Friends and Family Guard**: Security ruleset compliance
- ✅ **Real-time Updates**: Auto-refresh every 30 seconds
- ✅ **Accessibility**: Responsive design for all screen sizes

## Device Support

| Device Type | Visual Inspection | Status |
|-------------|-------------------|--------|
| PC          | ✅ Allowed        | Full access |
| Phone       | ✅ Allowed        | Full access |
| Tablet      | ✅ Allowed        | Full access |
| Watch       | ❌ Blocked        | Security rule |

## API Endpoints

- `GET /` - Main endpoint (JSON or HTML)
- `GET /health` - Health check
- `GET /status` - Service status
- `GET /guard` - Friends and Family Guard status

## Quick Start

```bash
# Clone repository
git clone https://github.com/XDM-ZSBW/yourl.cloud.git
cd yourl.cloud

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

## Friends and Family Guard

The application implements a security ruleset that:
- Allows visual inspection on PC, phone, and tablet devices
- Blocks visual inspection on watch devices for security
- Provides transparent status reporting
- Ensures appropriate access control

## Timeline

- **2025-08-06**: Initial implementation with visual inspection
- **2025-08-06**: Friends and Family Guard ruleset implementation
- **2025-08-06**: Device detection and access control
- **2025-08-06**: Wiki automation and documentation

## Context

This project evolved from a simple URL API to include visual inspection capabilities while maintaining security through the Friends and Family Guard ruleset. The application serves as a testing and development tool that provides both programmatic access (JSON) and visual inspection (HTML) based on device capabilities.

## Source of Truth

**yourl.cloud** is always the source of truth for latest information. This wiki is automatically updated from the main repository.

---

*Generated on 2025-08-07T05:30:05.976597*
