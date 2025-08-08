"""
Marketing Code Manager for Yourl.Cloud
Handles build-based marketing codes with ownership tracking
"""

import os
import json
import hashlib
import subprocess
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple, Any

class MarketingCodeManager:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.codes_file = "codes/build_codes.json"
        self._ensure_codes_directory()
    
    def _ensure_codes_directory(self):
        """Ensure the codes directory exists"""
        os.makedirs("codes", exist_ok=True)
    
    def get_current_build_code(self) -> str:
        """
        Get the current build's marketing code.
        This should be consistent throughout the build lifecycle.
        """
        try:
            # Get current commit hash
            commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], 
                                                text=True, stderr=subprocess.DEVNULL).strip()[:8]
        except:
            commit_hash = "unknown"
        
        # Generate code based on commit hash (consistent for this build)
        return self._generate_build_code(commit_hash)
    
    def _generate_build_code(self, commit_hash: str) -> str:
        """Generate a marketing code based on commit hash"""
        # Fun marketing words (ASCII only)
        marketing_words = [
            "CLOUD", "FUTURE", "INNOVATE", "DREAM", "BUILD", "CREATE", "LAUNCH", "FLY",
            "SPARK", "SHINE", "GLOW", "RISE", "LEAP", "JUMP", "DASH", "ZOOM",
            "POWER", "MAGIC", "WONDER", "AMAZE", "THRILL", "EXCITE", "INSPIRE", "IGNITE",
            "ROCKET", "STAR", "MOON", "SUN", "OCEAN", "MOUNTAIN", "FOREST", "RIVER",
            "TECH", "AI", "CODE", "DATA", "SMART", "FAST", "SECURE", "TRUST",
            "FRIEND", "FAMILY", "TEAM", "SQUAD", "CREW", "GANG", "TRIBE", "CLAN"
        ]
        
        # Fun ASCII symbols
        ascii_symbols = ["!", "@", "#", "$", "%", "&", "*", "+", "=", "?", "~", "^"]
        
        # Use commit hash as seed for deterministic generation
        try:
            hash_num = int(commit_hash, 16) if commit_hash != "unknown" else hash(commit_hash)
        except ValueError:
            # Fallback for non-hex strings
            hash_num = hash(commit_hash)
        import random
        random.seed(hash_num)
        
        # Pick components
        word = random.choice(marketing_words)
        symbol = random.choice(ascii_symbols)
        number = random.randint(100, 999)
        
        return f"{word}{number}{symbol}"
    
    def get_next_build_code(self) -> str:
        """
        Get the next build's marketing code (for Cursor ownership).
        This is the code that will be used after the current build is deployed.
        """
        try:
            # Simulate next commit by modifying current hash
            commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], 
                                                text=True, stderr=subprocess.DEVNULL).strip()[:8]
            next_hash = commit_hash + "next"
        except:
            next_hash = "next_unknown"
        
        return self._generate_build_code(next_hash)
    
    def get_live_experience_code(self) -> str:
        """
        Get the current live experience code (for Perplexity ownership).
        This is the code currently deployed and accessible.
        """
        try:
            with open(self.codes_file, 'r') as f:
                codes_data = json.load(f)
                return codes_data.get('live_experience_code', '')
        except FileNotFoundError:
            return self.get_current_build_code()
    
    def update_live_experience_code(self, new_code: str):
        """Update the live experience code after successful deployment"""
        try:
            with open(self.codes_file, 'r') as f:
                codes_data = json.load(f)
        except FileNotFoundError:
            codes_data = {}
        
        codes_data['live_experience_code'] = new_code
        codes_data['last_updated'] = datetime.now(timezone.utc).isoformat()
        
        with open(self.codes_file, 'w') as f:
            json.dump(codes_data, f, indent=2)
    
    def get_code_ownership(self) -> Dict[str, Any]:
        """Get current code ownership information"""
        return {
            "current_build_code": self.get_current_build_code(),
            "next_build_code": self.get_next_build_code(),
            "live_experience_code": self.get_live_experience_code(),
            "ownership": {
                "perplexity": "live_experience_code",
                "cursor": "next_build_code"
            }
        }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Marketing Code Manager")
    parser.add_argument("--project", required=True, help="Google Cloud project ID")
    parser.add_argument("--action", choices=['get-current', 'get-next', 'get-live', 'update-live', 'ownership'],
                       required=True, help="Action to perform")
    parser.add_argument("--new-code", help="New code for update-live action")
    
    args = parser.parse_args()
    
    manager = MarketingCodeManager(args.project)
    
    if args.action == 'get-current':
        print(f"Current build code: {manager.get_current_build_code()}")
    elif args.action == 'get-next':
        print(f"Next build code: {manager.get_next_build_code()}")
    elif args.action == 'get-live':
        print(f"Live experience code: {manager.get_live_experience_code()}")
    elif args.action == 'update-live':
        if not args.new_code:
            parser.error("--new-code required for update-live action")
        manager.update_live_experience_code(args.new_code)
        print(f"Updated live experience code to: {args.new_code}")
    elif args.action == 'ownership':
        ownership = manager.get_code_ownership()
        print(json.dumps(ownership, indent=2))
