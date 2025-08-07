#!/usr/bin/env python3
"""
README Update Script - Linear Progression Maintenance
===================================================

Script to ensure README.md is always kept current with linear progression updates.
Maintains README.md as the primary source of truth for current project state.

Author: Yourl Cloud Inc.
Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
Organization: Yourl Cloud Inc.
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path

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

def extract_current_features():
    """Extract current features from app.py."""
    app_content = read_file_content('app.py')
    if not app_content:
        return []
    
    features = []
    
    # Extract features based on code patterns
    if 'CLOUD_RUN_CONFIG' in app_content:
        features.append("🌐 **Domain Mapping**: Full Cloud Run domain mapping compatibility")
    
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
    
    return features

def get_current_version():
    """Get current version from app.py or default."""
    app_content = read_file_content('app.py')
    if app_content:
        # Look for version in app.py
        version_match = re.search(r'"version":\s*"([^"]+)"', app_content)
        if version_match:
            return version_match.group(1)
    
    return "1.0.0"

def update_readme():
    """Update README.md with current project information."""
    print("Starting README.md update...")
    
    # Get current information
    timestamp = datetime.utcnow().isoformat()
    features = extract_current_features()
    version = get_current_version()
    
    # Read current README
    readme_content = read_file_content('README.md')
    if not readme_content:
        print("README.md not found")
        return False
    
    # Simple string replacements instead of complex regex
    updated_readme = readme_content
    
    # Update version if found
    if '**Version**:' in updated_readme:
        updated_readme = re.sub(r'\*\*Version\*\*: \d+\.\d+\.\d+', f'**Version**: {version}', updated_readme)
    
    # Update last modified timestamp if found
    if '**Last Updated**:' in updated_readme:
        updated_readme = re.sub(r'\*\*Last Updated\*\*: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*?Z', f'**Last Updated**: {timestamp}', updated_readme)
    
    # Update features section if it exists
    if features and '## ✅ Current Features' in updated_readme:
        features_section = "\n".join(f"- {feature}" for feature in features)
        # Find the features section and replace it
        start_marker = "## ✅ Current Features"
        end_marker = "## "
        
        start_idx = updated_readme.find(start_marker)
        if start_idx != -1:
            end_idx = updated_readme.find(end_marker, start_idx + len(start_marker))
            if end_idx != -1:
                # Replace the features section
                before_features = updated_readme[:start_idx + len(start_marker)]
                after_features = updated_readme[end_idx:]
                updated_readme = before_features + "\n\n" + features_section + "\n" + after_features
    
    # Write updated README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(updated_readme)
    
    print("README.md updated successfully")
    return True

if __name__ == "__main__":
    update_readme()
