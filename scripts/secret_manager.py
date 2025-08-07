"""
Enhanced Google Cloud Secret Manager utility for yourl.cloud
Includes validation, rotation, and version management
"""

import os
import time
from datetime import datetime, timezone
from google.cloud import secretmanager
from google.api_core import retry
import subprocess

class SecretManager:
    def __init__(self, project_id=None):
        """Initialize Secret Manager client with project ID"""
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT')
        if not self.project_id:
            raise ValueError("Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable")
        self.client = secretmanager.SecretManagerServiceClient()
        self.sa_email = f"automation-sa-yourl@{self.project_id}.iam.gserviceaccount.com"

    @retry.Retry()
    def get_secret(self, secret_id, version_id="latest"):
        """
        Get secret value from Secret Manager with retry logic
        """
        try:
            name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
            response = self.client.access_secret_version(request={"name": name})
            # Log access without exposing value
            print(f"Accessed secret {secret_id} at {datetime.now(timezone.utc)}")
            return response.payload.data.decode("UTF-8")
        except Exception as e:
            print(f"Error accessing secret {secret_id}: {e.__class__.__name__}")
            raise

    def create_secret(self, secret_id, secret_value, labels=None):
        """
        Create a new secret with labels for tracking
        """
        try:
            parent = f"projects/{self.project_id}"
            
            # Default labels
            labels = labels or {
                "created_by": "automation-sa-yourl",
                "created_at": datetime.now(timezone.utc).strftime("%Y%m%d"),
                "managed_by": "yourl-cloud"
            }
            
            # Create the secret
            secret = self.client.create_secret(
                request={
                    "parent": parent,
                    "secret_id": secret_id,
                    "secret": {
                        "replication": {"automatic": {}},
                        "labels": labels,
                    },
                }
            )
            
            # Add the secret version
            version = self.client.add_secret_version(
                request={
                    "parent": secret.name,
                    "payload": {"data": secret_value.encode("UTF-8")},
                }
            )
            
            print(f"Created secret: {secret_id}")
            return secret.name
            
        except Exception as e:
            print(f"Error creating secret {secret_id}: {e.__class__.__name__}")
            raise

    def update_secret(self, secret_id, secret_value, reason="routine"):
        """
        Add a new version of a secret with audit trail
        """
        try:
            parent = f"projects/{self.project_id}/secrets/{secret_id}"
            
            # Add version with annotations
            version = self.client.add_secret_version(
                request={
                    "parent": parent,
                    "payload": {
                        "data": secret_value.encode("UTF-8"),
                        "annotations": {
                            "updated_by": self.sa_email,
                            "update_reason": reason,
                            "updated_at": datetime.now(timezone.utc).isoformat()
                        }
                    },
                }
            )
            
            print(f"Updated secret: {secret_id}")
            return version.name
            
        except Exception as e:
            print(f"Error updating secret {secret_id}: {e.__class__.__name__}")
            raise

    def validate_setup(self):
        """
        Validate service account and secret access
        Returns: (bool, str) - (success, message)
        """
        try:
            # Check service account exists
            result = subprocess.run(
                f"gcloud iam service-accounts describe {self.sa_email} --project={self.project_id}",
                shell=True, capture_output=True, text=True
            )
            if result.returncode != 0:
                return False, f"Service account validation failed: {result.stderr}"

            # Test secret access
            try:
                self.get_secret("SENDGRID_API_KEY")
            except Exception as e:
                return False, f"Secret access validation failed: {str(e)}"

            return True, "Validation successful"
        except Exception as e:
            return False, f"Validation failed: {str(e)}"

    def list_versions(self, secret_id):
        """
        List all versions of a secret
        """
        try:
            parent = f"projects/{self.project_id}/secrets/{secret_id}"
            versions = self.client.list_secret_versions(request={"parent": parent})
            
            results = []
            for version in versions:
                results.append({
                    "version": version.name.split("/")[-1],
                    "state": version.state.name,
                    "create_time": version.create_time.isoformat()
                })
            return results
        except Exception as e:
            print(f"Error listing versions for {secret_id}: {e.__class__.__name__}")
            raise

    def rotate_secret(self, secret_id, new_value):
        """
        Rotate a secret value and disable old versions
        """
        try:
            # Add new version
            new_version = self.update_secret(secret_id, new_value, reason="rotation")
            
            # List and disable old versions
            parent = f"projects/{self.project_id}/secrets/{secret_id}"
            versions = self.client.list_secret_versions(request={"parent": parent})
            
            for version in versions:
                if version.name != new_version and version.state == secretmanager.SecretVersion.State.ENABLED:
                    self.client.disable_secret_version(request={"name": version.name})
            
            print(f"Rotated secret: {secret_id}")
            return new_version
        except Exception as e:
            print(f"Error rotating secret {secret_id}: {e.__class__.__name__}")
            raise

def get_secret(secret_id, project_id=None):
    """
    Convenience function to get a secret value
    """
    manager = SecretManager(project_id)
    return manager.get_secret(secret_id)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage secrets in Google Cloud Secret Manager")
    parser.add_argument("--project", help="Google Cloud project ID")
    parser.add_argument("--action", choices=["create", "update", "get", "rotate", "validate", "list-versions"],
                      required=True, help="Action to perform")
    parser.add_argument("--secret-id", required=True, help="ID of the secret")
    parser.add_argument("--value-file", help="File containing the secret value")
    parser.add_argument("--reason", help="Reason for update (for audit trail)")
    
    args = parser.parse_args()
    
    try:
        manager = SecretManager(args.project)
        
        if args.action in ["create", "update", "rotate"]:
            if not args.value_file:
                raise ValueError("--value-file required for create/update/rotate actions")
            
            with open(args.value_file, "r") as f:
                secret_value = f.read().strip()
            
            if args.action == "create":
                manager.create_secret(args.secret_id, secret_value)
            elif args.action == "update":
                manager.update_secret(args.secret_id, secret_value, args.reason or "manual-update")
            else:  # rotate
                manager.rotate_secret(args.secret_id, secret_value)
        
        elif args.action == "get":
            # Only print success/failure, never the actual value
            manager.get_secret(args.secret_id)
            print(f"Successfully retrieved secret: {args.secret_id}")
        
        elif args.action == "validate":
            success, message = manager.validate_setup()
            print(f"Validation {'succeeded' if success else 'failed'}: {message}")
        
        elif args.action == "list-versions":
            versions = manager.list_versions(args.secret_id)
            print(f"\nVersions for secret {args.secret_id}:")
            for v in versions:
                print(f"Version: {v['version']}")
                print(f"State: {v['state']}")
                print(f"Created: {v['create_time']}")
                print("---")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)