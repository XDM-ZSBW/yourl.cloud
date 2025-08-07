#!/usr/bin/env python3
"""
Auto Update Script - Comprehensive Documentation Synchronization
===============================================================

Automated script that ensures both wiki and README.md are always kept current.
Handles linear progression updates for README.md and past/present/future context for wiki.

Author: Yourl Cloud Inc.
Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
Organization: Yourl Cloud Inc.
"""

import os
import sys
import subprocess
from datetime import datetime, timezone
from pathlib import Path

def run_script(script_name, description):
    """Run a Python script and handle errors."""
    print(f"Running {description}...")
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print(f"{description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"{description} failed with exception: {e}")
        return False

def check_git_status():
    """Check if we're in a git repository and get current status."""
    try:
        # Check if we're in a git repository
        subprocess.run(['git', 'rev-parse', '--git-dir'], 
                      check=True, capture_output=True)
        
        # Get current branch
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                                       text=True).strip()
        
        # Get last commit hash
        commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], 
                                            text=True).strip()[:8]
        
        print(f"Git Repository: {branch} ({commit_hash})")
        return True
    except subprocess.CalledProcessError:
        print("Not in a git repository")
        return False
    except Exception as e:
        print(f"Could not check git status: {e}")
        return False

def create_git_hook():
    """Create git hook for automatic updates."""
    hook_content = """#!/bin/sh
# Git hook to automatically update documentation after commits

echo "Auto-updating documentation after commit..."
python auto_update.py --post-commit

if [ $? -eq 0 ]; then
    echo "Documentation updated successfully"
else
    echo "Documentation update failed"
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
    
    print(f"Git hook created: {hook_file}")

def main():
    """Main function to handle auto-updates."""
    print("Starting comprehensive documentation update...")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    
    # Check git status
    in_git = check_git_status()
    
    # Check if we're in post-commit mode
    is_post_commit = len(sys.argv) > 1 and sys.argv[1] == "--post-commit"
    
    # Update README.md (linear progression)
    readme_success = run_script("scripts/update_readme.py", "Updating README.md (linear progression)")
    
    # Update wiki (past/present/future context) - only if not in post-commit mode
    if is_post_commit:
        print("Skipping wiki update in post-commit mode to avoid sync issues")
        wiki_success = True
    else:
        wiki_success = run_script("scripts/update_wiki.py", "Updating wiki (past/present/future context)")
    
    # Summary
    print("\n" + "="*60)
    print("Update Summary:")
    print(f"   README.md: {'Success' if readme_success else 'Failed'}")
    print(f"   Wiki: {'Success' if wiki_success else 'Failed'}")
    print(f"   Git Repository: {'Detected' if in_git else 'Not detected'}")
    
    if readme_success and wiki_success:
        print("\nAll documentation updated successfully!")
        print("README.md: Linear progression maintained")
        if not is_post_commit:
            print("Wiki: Past, present, and future context included")
        print("yourl.cloud is always the source of truth")
        return True
    else:
        print("\nSome updates failed. Please check the errors above.")
        return False

def setup_automation():
    """Set up automation for the project."""
    print("Setting up documentation automation...")
    
    # Create git hook
    create_git_hook()
    
    # Test the update scripts
    print("\nTesting update scripts...")
    test_success = main()
    
    if test_success:
        print("\nAutomation setup completed successfully!")
        print("Documentation will now update automatically after each commit.")
    else:
        print("\nAutomation setup completed with warnings.")
        print("Some updates may need manual intervention.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup":
            setup_automation()
        elif sys.argv[1] == "--post-commit":
            # Run in post-commit mode (quiet)
            success = main()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "--help":
            print("""
Auto Update Script - Documentation Synchronization

Usage:
  python auto_update.py           # Run full update
  python auto_update.py --setup   # Set up automation
  python auto_update.py --help    # Show this help

Features:
  - Updates README.md with linear progression
  - Updates wiki with past/present/future context
  - Automatic updates after git commits
  - Comprehensive error handling
  - Git hook integration

Author: Yourl Cloud Inc.
""")
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for usage information.")
    else:
        main()
