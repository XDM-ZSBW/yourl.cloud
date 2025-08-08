#!/usr/bin/env python3
"""
Update Live Experience Code Script
Updates the live experience code after successful deployment
"""

import os
import sys
import subprocess
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.marketing_code_manager import MarketingCodeManager

def update_live_code_after_deployment():
    """Update the live experience code after successful deployment"""
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'root-wharf-383822')
    
    try:
        manager = MarketingCodeManager(project_id)
        
        # Get the current build code (what should become the live code)
        current_build_code = manager.get_current_build_code()
        
        # Update the live experience code
        manager.update_live_experience_code(current_build_code)
        
        print(f"✅ Updated live experience code to: {current_build_code}")
        print(f"📝 This code is now visible to Perplexity and all users")
        
        # Show ownership information
        ownership = manager.get_code_ownership()
        print(f"\n📊 Current Code Ownership:")
        print(f"   Live Experience (Perplexity): {ownership['live_experience_code']}")
        print(f"   Next Build (Cursor): {ownership['next_build_code']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating live experience code: {e}")
        return False

def show_current_ownership():
    """Show current code ownership information"""
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'root-wharf-383822')
    
    try:
        manager = MarketingCodeManager(project_id)
        ownership = manager.get_code_ownership()
        
        print(f"📊 Current Code Ownership:")
        print(f"   Live Experience (Perplexity): {ownership['live_experience_code']}")
        print(f"   Next Build (Cursor): {ownership['next_build_code']}")
        print(f"   Current Build: {ownership['current_build_code']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error getting ownership info: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Update Live Experience Code")
    parser.add_argument("--action", choices=['update', 'show'], default='show',
                       help="Action to perform")
    
    args = parser.parse_args()
    
    if args.action == 'update':
        success = update_live_code_after_deployment()
        sys.exit(0 if success else 1)
    elif args.action == 'show':
        success = show_current_ownership()
        sys.exit(0 if success else 1)
