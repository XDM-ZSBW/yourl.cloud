#!/usr/bin/env python3
"""
Wiki Update Script - Comprehensive Wiki Synchronization
======================================================

Advanced script to automatically update the GitHub wiki with current project information.
Ensures wiki stays synchronized with main repository and includes past, present, and future context.

Author: Yourl Cloud Inc.
Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
Organization: Yourl Cloud Inc.
Domain Mapping: Compatible
Cloud Run: Supported
"""

import os
import sys
import json
import subprocess
import re
from datetime import datetime, timedelta
from pathlib import Path

def get_git_info():
    """Get current git information."""
    try:
        # Get current branch
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                                       text=True, stderr=subprocess.DEVNULL).strip()
        
        # Get last commit hash
        commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], 
                                            text=True, stderr=subprocess.DEVNULL).strip()[:8]
        
        # Get last commit date
        commit_date = subprocess.check_output(['git', 'log', '-1', '--format=%cd', '--date=iso'], 
                                            text=True, stderr=subprocess.DEVNULL).strip()
        
        return {
            'branch': branch,
            'commit_hash': commit_hash,
            'commit_date': commit_date
        }
    except Exception as e:
        print(f"Warning: Could not get git info: {e}")
        return {
            'branch': 'unknown',
            'commit_hash': 'unknown',
            'commit_date': datetime.utcnow().isoformat()
        }

def read_file_content(file_path):
    """Read file content safely."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def extract_features_from_app():
    """Extract current features from app.py."""
    app_content = read_file_content('app.py')
    if not app_content:
        return []
    
    features = []
    
    # Extract features based on code patterns
    if 'CLOUD_RUN_CONFIG' in app_content:
        features.append("🌐 **Cloud Run Domain Mapping**: Full compatibility with custom domains")
    
    if 'FRIENDS_FAMILY_GUARD' in app_content:
        features.append("🛡️ **Friends and Family Guard**: Security ruleset compliance")
    
    if 'visual_inspection' in app_content:
        features.append("👁️ **Visual Inspection**: Modern web interface for allowed devices")
    
    if 'device_type' in app_content:
        features.append("📱 **Device Detection**: Automatic detection of PC, phone, tablet, watch")
    
    if 'health_check' in app_content:
        features.append("🏥 **Health Checks**: Cloud Run compatible health endpoints")
    
    if 'X-Forwarded' in app_content:
        features.append("🔗 **X-Forwarded Headers**: Proper proxy header handling")
    
    if 'gunicorn' in app_content or 'waitress' in app_content:
        features.append("🚀 **WSGI Server**: Production-ready Gunicorn/Waitress support")
    
    if 'domain_mapping' in app_content:
        features.append("🌍 **Domain Mapping**: Custom domain support (yourl.cloud)")
    
    if 'generate_marketing_password' in app_content:
        features.append("🎪 **Dynamic Marketing Passwords**: ASCII-only passwords that change with each commit")
    
    return features

def get_current_marketing_password_from_app():
    """Get the current marketing password from app.py."""
    try:
        # Import the function from app.py
        import sys
        import os
        sys.path.append(os.getcwd())
        from app import get_current_marketing_password
        return get_current_marketing_password()
    except Exception as e:
        return "AI474?"  # Fallback password if import fails

def get_project_timeline():
    """Get project timeline from git history and current state."""
    timeline = []
    
    try:
        # Get recent commits
        commits = subprocess.check_output(['git', 'log', '--oneline', '--since=30 days'], 
                                        text=True, stderr=subprocess.DEVNULL).strip().split('\n')
        
        for commit in commits[:10]:  # Last 10 commits
            if commit:
                parts = commit.split(' ', 1)
                if len(parts) == 2:
                    hash_part = parts[0]
                    message = parts[1]
                    timeline.append(f"**{hash_part}**: {message}")
    
    except Exception as e:
        print(f"Warning: Could not get git timeline: {e}")
    
    # Add current state
    timeline.append(f"**{datetime.utcnow().strftime('%Y-%m-%d')}**: Current - Cloud Run Domain Mapping Implementation")
    
    return timeline

def create_wiki_content():
    """Create comprehensive wiki content from current project state."""
    
    # Get current information
    git_info = get_git_info()
    timestamp = datetime.utcnow().isoformat()
    features = extract_features_from_app()
    timeline = get_project_timeline()
    
    # Read current files
    readme_content = read_file_content('README.md')
    app_content = read_file_content('app.py')
    status_content = read_file_content('STATUS.md')
    
    # Create comprehensive wiki content
    wiki_content = f"""# Yourl.Cloud - URL API Server with Visual Inspection

**Last Updated**: {timestamp}
**Session ID**: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
**Organization**: Yourl Cloud Inc.
**Branch**: {git_info['branch']}
**Commit**: {git_info['commit_hash']}
**Commit Date**: {git_info['commit_date']}

## 🎯 Project Overview

Yourl.Cloud is a production-ready Python Flask API that returns the request URL with advanced visual inspection capabilities. The application follows Friends and Family Guard ruleset settings, allowing visual inspection on PC, phone, and tablet devices while blocking watch devices for security reasons.

**Key Innovation**: Full Google Cloud Run domain mapping compatibility with automatic X-Forwarded header support.

## ✅ Current Features

{chr(10).join(f"- {feature}" for feature in features)}

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
gcloud run deploy yourl-cloud \\
  --image gcr.io/$PROJECT_ID/yourl-cloud:latest \\
  --region=us-west1 \\
  --platform=managed \\
  --allow-unauthenticated \\
  --port=8080

# Map custom domain
gcloud run domain-mappings create \\
  --service yourl-cloud \\
  --domain yourl.cloud \\
  --region us-west1 \\
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

## 🎪 Marketing Password System

The application features a dynamic, fun marketing password system that changes with each commit:

### 🎯 Current Marketing Password
**`{get_current_marketing_password_from_app()}`** - Generated for this commit!

### ✨ Password Features
- **Dynamic Generation**: Changes with every code commit
- **ASCII-Only**: Uses basic ASCII characters for maximum compatibility
- **Marketing-Friendly**: Fun, memorable combinations
- **Public-Safe**: Safe for public sharing and marketing
- **Auto-Display**: Shown on landing page for easy access

### 🎊 Password Format
**Format**: `MARKETING_WORD + 2-3_DIGIT_NUMBER + ASCII_SYMBOL`

**Examples**:
- `CLOUD123!` - Cloud computing theme
- `FUTURE456@` - Future-focused
- `MAGIC789#` - Magical experience
- `ROCKET321$` - Rocket-powered

### 🔄 How It Works
1. **Commit-Based**: Uses git commit hash for deterministic generation
2. **Fun Words**: Marketing-friendly words like CLOUD, FUTURE, MAGIC, ROCKET
3. **ASCII Symbols**: Uses !@#$%&*+=?~^ for fun characters
4. **Auto-Update**: Changes automatically with each commit

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
CLOUD_RUN_CONFIG = {{
    "domain_mapping_enabled": True,
    "region": "us-west1",
    "trust_proxy": True,
    "cors_enabled": True,
    "health_check_path": "/health",
    "readiness_check_path": "/health"
}}
```

## 📅 Timeline

### Recent Development
{chr(10).join(f"- {item}" for item in timeline[:5])}

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

*Generated on {timestamp} | Branch: {git_info['branch']} | Commit: {git_info['commit_hash']}*
"""
    
    return wiki_content

def update_wiki():
    """Update the wiki with current content."""
    print("Starting comprehensive wiki update...")
    
    # Create wiki content
    wiki_content = create_wiki_content()
    
    # Write to wiki file
    wiki_file = "wiki/Home.md"
    os.makedirs("wiki", exist_ok=True)
    
    with open(wiki_file, 'w', encoding='utf-8') as f:
        f.write(wiki_content)
    
    print(f"Wiki updated: {wiki_file}")
    print("Remember: yourl.cloud is always the source of truth")
    print("Wiki includes: Past, Present, and Future context")
    
    return wiki_content

def create_wiki_update_hook():
    """Create a git hook to automatically update wiki after commits."""
    hook_content = """#!/bin/sh
# Git hook to automatically update wiki after commits

echo "🔄 Auto-updating wiki after commit..."
python update_wiki.py

if [ $? -eq 0 ]; then
    echo "✅ Wiki updated successfully"
else
    echo "❌ Wiki update failed"
fi
"""
    
    # Create .git/hooks directory if it doesn't exist
    hooks_dir = ".git/hooks"
    os.makedirs(hooks_dir, exist_ok=True)
    
    # Write post-commit hook
    hook_file = os.path.join(hooks_dir, "post-commit")
    with open(hook_file, 'w') as f:
        f.write(hook_content)
    
    # Make it executable
    os.chmod(hook_file, 0o755)
    
    print(f"✅ Git hook created: {hook_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--setup-hook":
        create_wiki_update_hook()
    else:
        update_wiki()
