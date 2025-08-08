#!/usr/bin/env python3
"""
Deployment Script with Code Rotation for Yourl.Cloud
Handles deployment, code rotation, and database logging
"""

import os
import sys
import subprocess
import json
from datetime import datetime, timezone
from typing import Dict, Optional, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.secret_manager_client import SecretManagerClient
from scripts.database_client import DatabaseClient
from scripts.marketing_code_manager import MarketingCodeManager

class DeploymentManager:
    def __init__(self, project_id: str, database_connection_string: Optional[str] = None):
        self.project_id = project_id
        self.secret_client = SecretManagerClient(project_id)
        self.marketing_manager = MarketingCodeManager(project_id)
        self.database_client = None
        
        if database_connection_string:
            self.database_client = DatabaseClient(database_connection_string)
    
    def generate_new_codes(self) -> Dict[str, str]:
        """Generate new current and next codes"""
        current_build_code = self.marketing_manager.get_current_build_code()
        next_build_code = self.marketing_manager.get_next_build_code()
        
        return {
            "current": current_build_code,
            "next": next_build_code
        }
    
    def rotate_codes(self) -> bool:
        """Rotate codes: next becomes current, generate new next"""
        try:
            # Get current next code (will become current)
            current_next_code = self.secret_client.get_next_marketing_code()
            if not current_next_code:
                print("❌ No next code found in Secret Manager")
                return False
            
            # Generate new codes
            new_codes = self.generate_new_codes()
            
            # Rotate codes in Secret Manager
            success = self.secret_client.rotate_codes(
                new_current_code=current_next_code,
                new_next_code=new_codes["next"]
            )
            
            if success:
                print(f"✅ Code rotation successful:")
                print(f"   Current (live): {current_next_code}")
                print(f"   Next: {new_codes['next']}")
                
                # Log to database if available
                if self.database_client:
                    self.database_client.log_code_history(
                        code=current_next_code,
                        code_type="current",
                        commit_hash=self._get_commit_hash(),
                        deployment_id=self._get_deployment_id(),
                        rotation_reason="deployment"
                    )
                
                return True
            else:
                print("❌ Code rotation failed")
                return False
                
        except Exception as e:
            print(f"❌ Error during code rotation: {e}")
            return False
    
    def initialize_secrets(self) -> bool:
        """Initialize secrets if they don't exist"""
        try:
            # Generate initial codes
            codes = self.generate_new_codes()
            
            # Set current code
            if not self.secret_client.get_current_marketing_code():
                success = self.secret_client.set_current_marketing_code(codes["current"])
                if not success:
                    print("❌ Failed to set current code")
                    return False
            
            # Set next code
            if not self.secret_client.get_next_marketing_code():
                success = self.secret_client.set_next_marketing_code(codes["next"])
                if not success:
                    print("❌ Failed to set next code")
                    return False
            
            print("✅ Secrets initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing secrets: {e}")
            return False
    
    def deploy_to_cloud_run(self) -> bool:
        """Deploy to Google Cloud Run"""
        try:
            print("🚀 Deploying to Google Cloud Run...")
            
            # Build and deploy
            cmd = [
                "gcloud", "run", "deploy", "yourl-cloud",
                "--source", ".",
                "--region", "us-west1",
                "--allow-unauthenticated",
                "--port", "8080",
                "--min-instances", "1",
                "--set-env-vars", f"GOOGLE_CLOUD_PROJECT={self.project_id}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Deployment successful")
                return True
            else:
                print(f"❌ Deployment failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error during deployment: {e}")
            return False
    
    def _get_commit_hash(self) -> Optional[str]:
        """Get current commit hash"""
        try:
            result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()[:8]
        except:
            pass
        return None
    
    def _get_deployment_id(self) -> str:
        """Generate deployment ID"""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        commit_hash = self._get_commit_hash() or "unknown"
        return f"deploy-{timestamp}-{commit_hash}"
    
    def get_deployment_status(self) -> Dict[str, Any]:
        """Get current deployment and code status"""
        try:
            # Get service URL
            cmd = ["gcloud", "run", "services", "describe", "yourl-cloud", 
                   "--region", "us-west1", "--format", "value(status.url)"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            service_url = result.stdout.strip() if result.returncode == 0 else None
            
            # Get code metadata
            code_metadata = self.secret_client.get_code_metadata()
            
            return {
                "project_id": self.project_id,
                "service_url": service_url,
                "deployment_id": self._get_deployment_id(),
                "commit_hash": self._get_commit_hash(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "codes": code_metadata
            }
            
        except Exception as e:
            print(f"❌ Error getting deployment status: {e}")
            return {}

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Deployment Manager")
    parser.add_argument("--project", required=True, help="Google Cloud project ID")
    parser.add_argument("--action", choices=['deploy', 'rotate', 'init', 'status'],
                       required=True, help="Action to perform")
    parser.add_argument("--database-connection", help="Database connection string")
    
    args = parser.parse_args()
    
    manager = DeploymentManager(args.project, args.database_connection)
    
    if args.action == 'init':
        success = manager.initialize_secrets()
        sys.exit(0 if success else 1)
        
    elif args.action == 'rotate':
        success = manager.rotate_codes()
        sys.exit(0 if success else 1)
        
    elif args.action == 'deploy':
        # First rotate codes
        if not manager.rotate_codes():
            print("❌ Code rotation failed, aborting deployment")
            sys.exit(1)
        
        # Then deploy
        success = manager.deploy_to_cloud_run()
        sys.exit(0 if success else 1)
        
    elif args.action == 'status':
        status = manager.get_deployment_status()
        print(json.dumps(status, indent=2))
        sys.exit(0)

if __name__ == "__main__":
    main()
