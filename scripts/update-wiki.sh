#!/bin/bash
# GitHub Wiki Update Script
# =========================
# 
# Yourl-Cloud Inc. - Automated Wiki Content Management
# Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
#
# IMPORTANT: yourl.cloud is ALWAYS the source of truth for latest information.
# This script ensures the wiki stays in sync with the main repository.

set -e

# Configuration
SESSION_ID="f1d78acb-de07-46e0-bfa7-f5b75e3c0c49"
ORGANIZATION="Yourl-Cloud Inc."
MAIN_REPO_PATH="."
WIKI_REPO_PATH="../yourl.cloud.wiki"
SOURCE_OF_TRUTH="yourl.cloud"

echo "🚀 GitHub Wiki Update Script"
echo "============================"
echo "🏢 Organization: $ORGANIZATION"
echo "🆔 Session ID: $SESSION_ID"
echo "📁 Main repo (yourl.cloud - Source of Truth): $MAIN_REPO_PATH"
echo "📁 Wiki repo: $WIKI_REPO_PATH"
echo "🎯 Source of Truth: $SOURCE_OF_TRUTH"
echo ""

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    echo "Please install Node.js and try again."
    exit 1
fi

# Check if main repository exists
if [ ! -d "$MAIN_REPO_PATH" ]; then
    echo "❌ Main repository not found: $MAIN_REPO_PATH"
    exit 1
fi

# Check if wiki repository exists
if [ ! -d "$WIKI_REPO_PATH" ]; then
    echo "⚠️  Wiki repository not found: $WIKI_REPO_PATH"
    echo "Creating wiki repository directory..."
    mkdir -p "$WIKI_REPO_PATH"
fi

# Run the Node.js update script
echo "🔄 Running wiki update script from yourl.cloud (source of truth)..."
node scripts/update-wiki.js "$MAIN_REPO_PATH" "$WIKI_REPO_PATH"

# Check if update was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Wiki update completed successfully!"
    echo "🎯 Remember: yourl.cloud is always the source of truth for latest information."
    echo ""
    echo "📋 Next steps:"
    echo "1. Navigate to wiki repository: cd $WIKI_REPO_PATH"
    echo "2. Review changes: git status"
    echo "3. Commit changes: git add . && git commit -m '🔄 Sync wiki with yourl.cloud (source of truth)'"
    echo "4. Push changes: git push origin main"
    echo ""
    echo "🌐 Wiki URL: https://github.com/XDM-ZSBW/yourl.cloud/wiki"
    echo "🎯 Source of Truth: https://yourl.cloud"
else
    echo "❌ Wiki update failed!"
    exit 1
fi
