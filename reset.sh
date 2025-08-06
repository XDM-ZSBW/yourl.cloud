#!/bin/bash
# yourl.cloud Reset Script (Unix/Linux/macOS)
# Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

echo "yourl.cloud - Reset Script"
echo "=========================="
echo "Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49"
echo "Timestamp: $(date -u '+%Y-%m-%d %H:%M:%S') UTC"
echo ""

echo "Resetting yourl.cloud to clean state..."
echo ""

# Clear any cached data
if [ -d ".cache" ]; then
    echo "Clearing cache directory..."
    rm -rf .cache
fi

# Reset git status (if needed)
if [ -d ".git" ]; then
    echo "Checking git status..."
    git status --porcelain
    echo ""
fi

# Show current files
echo "Current project files:"
ls -la | grep -E '\.(html|md|sh|bat)$|^reset$|^status$'
echo ""

echo "Reset complete. Essential files maintained:"
echo "- index.html"
echo "- README.md" 
echo "- reset.sh"
echo "- reset.bat"
echo "- reset"
echo "- status"
echo ""
echo "For more information: https://github.com/XDM-ZSBW/yourl.cloud"
