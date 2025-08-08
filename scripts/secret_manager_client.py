#!/usr/bin/env python3
"""
Google Secret Manager Client for Yourl.Cloud Marketing Codes
Handles secure storage and retrieval of marketing codes
"""

import os
import json
import time
from datetime import datetime, timezone
from typing import Dict, Optional, Any, List
from google.cloud import secretmanager
from google.api_core import exceptions

class SecretManagerClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()
        
        # Secret names
        self.current_code_secret = f"projects/{project_id}/secrets/yourl_marketing_code_current"
        self.next_code_secret = f"projects/{project_id}/secrets/yourl_marketing_code_next"
        
    def _get_secret_version(self, secret_name: str, version: str = "latest") -> Optional[str]:
        """Get a secret version"""
        try:
            name = f"{secret_name}/versions/{version}"
            response = self.client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except exceptions.NotFound:
            return None
        except Exception as e:
            print(f"Error accessing secret {secret_name}: {e}")
            return None
    
    def _create_secret(self, secret_name: str, description: str = "") -> bool:
        """Create a new secret"""
        try:
            parent = f"projects/{self.project_id}"
            secret_id = secret_name.split("/")[-1]
            
            secret = secretmanager.Secret()
            secret.replication.automatic = secretmanager.Replication.Automatic()
            
            if description:
                # Use a valid label key (lowercase, no spaces)
                secret.labels["purpose"] = description.lower().replace(" ", "_")
            
            self.client.create_secret(
                request={
                    "parent": parent,
                    "secret_id": secret_id,
                    "secret": secret,
                }
            )
            return True
        except exceptions.AlreadyExists:
            return True  # Secret already exists
        except Exception as e:
            print(f"Error creating secret {secret_name}: {e}")
            return False
    
    def _add_secret_version(self, secret_name: str, payload: str) -> bool:
        """Add a new version to a secret"""
        try:
            parent = secret_name
            payload_bytes = payload.encode("UTF-8")
            
            self.client.add_secret_version(
                request={
                    "parent": parent,
                    "payload": secretmanager.SecretPayload(data=payload_bytes),
                }
            )
            return True
        except Exception as e:
            print(f"Error adding secret version to {secret_name}: {e}")
            return False
    
    def get_current_marketing_code(self) -> Optional[str]:
        """Get the current live marketing code from Secret Manager"""
        return self._get_secret_version(self.current_code_secret)
    
    def get_next_marketing_code(self) -> Optional[str]:
        """Get the next marketing code from Secret Manager"""
        return self._get_secret_version(self.next_code_secret)
    
    def set_current_marketing_code(self, code: str) -> bool:
        """Set the current marketing code"""
        # Ensure secret exists
        if not self._create_secret(self.current_code_secret, "Current live marketing code"):
            return False
        
        # Add new version
        return self._add_secret_version(self.current_code_secret, code)
    
    def set_next_marketing_code(self, code: str) -> bool:
        """Set the next marketing code"""
        # Ensure secret exists
        if not self._create_secret(self.next_code_secret, "Next marketing code for deployment"):
            return False
        
        # Add new version
        return self._add_secret_version(self.next_code_secret, code)
    
    def rotate_codes(self, new_current_code: str, new_next_code: str) -> bool:
        """Rotate codes: current becomes archived, next becomes current, new next is set"""
        try:
            # Archive current code (keep for audit)
            current_code = self.get_current_marketing_code()
            if current_code:
                self._add_secret_version(self.current_code_secret, f"ARCHIVED_{current_code}")
            
            # Set new current code
            if not self.set_current_marketing_code(new_current_code):
                return False
            
            # Set new next code
            if not self.set_next_marketing_code(new_next_code):
                return False
            
            return True
        except Exception as e:
            print(f"Error rotating codes: {e}")
            return False
    
    def get_code_metadata(self) -> Dict[str, Any]:
        """Get metadata about current codes"""
        current_code = self.get_current_marketing_code()
        next_code = self.get_next_marketing_code()
        
        return {
            "current_code": current_code,
            "next_code": next_code,
            "project_id": self.project_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "secrets": {
                "current": self.current_code_secret,
                "next": self.next_code_secret
            }
        }
    
    def list_secret_versions(self, secret_name: str) -> List[Dict[str, Any]]:
        """List all versions of a secret for audit purposes"""
        try:
            parent = secret_name
            request = {"parent": parent}
            page_result = self.client.list_secret_versions(request=request)
            
            versions = []
            for version in page_result:
                versions.append({
                    "name": version.name,
                    "state": version.state.name,
                    "create_time": version.create_time.isoformat(),
                    "destroy_time": version.destroy_time.isoformat() if version.destroy_time else None
                })
            
            return versions
        except Exception as e:
            print(f"Error listing secret versions: {e}")
            return []

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Secret Manager Client")
    parser.add_argument("--project", required=True, help="Google Cloud project ID")
    parser.add_argument("--action", choices=['get-current', 'get-next', 'set-current', 'set-next', 'rotate', 'metadata', 'list-versions'],
                       required=True, help="Action to perform")
    parser.add_argument("--code", help="Code to set")
    parser.add_argument("--new-current", help="New current code for rotation")
    parser.add_argument("--new-next", help="New next code for rotation")
    parser.add_argument("--secret-name", help="Secret name for list-versions")
    
    args = parser.parse_args()
    
    client = SecretManagerClient(args.project)
    
    if args.action == 'get-current':
        code = client.get_current_marketing_code()
        print(f"Current marketing code: {code}")
        
    elif args.action == 'get-next':
        code = client.get_next_marketing_code()
        print(f"Next marketing code: {code}")
        
    elif args.action == 'set-current':
        if not args.code:
            parser.error("--code required for set-current action")
        success = client.set_current_marketing_code(args.code)
        print(f"Set current code: {'Success' if success else 'Failed'}")
        
    elif args.action == 'set-next':
        if not args.code:
            parser.error("--code required for set-next action")
        success = client.set_next_marketing_code(args.code)
        print(f"Set next code: {'Success' if success else 'Failed'}")
        
    elif args.action == 'rotate':
        if not all([args.new_current, args.new_next]):
            parser.error("--new-current and --new-next required for rotate action")
        success = client.rotate_codes(args.new_current, args.new_next)
        print(f"Code rotation: {'Success' if success else 'Failed'}")
        
    elif args.action == 'metadata':
        metadata = client.get_code_metadata()
        print(json.dumps(metadata, indent=2))
        
    elif args.action == 'list-versions':
        if not args.secret_name:
            parser.error("--secret-name required for list-versions action")
        versions = client.list_secret_versions(args.secret_name)
        print(json.dumps(versions, indent=2))
