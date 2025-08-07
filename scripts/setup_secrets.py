"""
Setup script for Google Cloud Secret Manager configuration
Automates service account creation and IAM setup
"""

import subprocess
import os
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error output: {e.stderr}")
        if check:
            sys.exit(1)
        return None

def setup_secret_manager(project_id, service_account_id):
    """
    Set up Secret Manager and service account
    
    Args:
        project_id: Google Cloud project ID
        service_account_id: ID for the service account (e.g., 'automation-sa-yourl')
    """
    print("\n=== Setting up Google Cloud Secret Manager ===\n")
    
    # Enable Secret Manager API
    print("Enabling Secret Manager API...")
    run_command(f"gcloud services enable secretmanager.googleapis.com --project={project_id}")
    
    # Create service account if it doesn't exist
    print("\nCreating service account...")
    sa_email = f"{service_account_id}@{project_id}.iam.gserviceaccount.com"
    result = run_command(
        f"gcloud iam service-accounts describe {sa_email} --project={project_id}",
        check=False
    )
    
    if not result:
        run_command(
            f"gcloud iam service-accounts create {service_account_id} "
            f"--display-name=\"Automation Service Account for yourl.cloud\" "
            f"--project={project_id}"
        )
        print(f"Created service account: {sa_email}")
    else:
        print(f"Service account already exists: {sa_email}")

def setup_secrets(project_id, service_account_id, secrets):
    """
    Create secrets and grant access to service account
    
    Args:
        project_id: Google Cloud project ID
        service_account_id: ID for the service account
        secrets: List of secret IDs to create
    """
    sa_email = f"{service_account_id}@{project_id}.iam.gserviceaccount.com"
    
    for secret_id in secrets:
        print(f"\nSetting up secret: {secret_id}")
        
        # Create secret if it doesn't exist
        result = run_command(
            f"gcloud secrets describe {secret_id} --project={project_id}",
            check=False
        )
        
        if not result:
            run_command(
                f"gcloud secrets create {secret_id} "
                f"--replication-policy=automatic "
                f"--project={project_id}"
            )
            print(f"Created secret: {secret_id}")
        else:
            print(f"Secret already exists: {secret_id}")
        
        # Grant access to service account
        print(f"Granting access to {sa_email}...")
        run_command(
            f"gcloud secrets add-iam-policy-binding {secret_id} "
            f"--member=\"serviceAccount:{sa_email}\" "
            f"--role=\"roles/secretmanager.secretAccessor\" "
            f"--project={project_id}"
        )

def update_cloudbuild_yaml():
    """Update cloudbuild.yaml to use service account and secrets"""
    cloudbuild_path = Path("cloudbuild.yaml")
    if not cloudbuild_path.exists():
        print("\nError: cloudbuild.yaml not found")
        return
    
    with open(cloudbuild_path, "r") as f:
        content = f.read()
    
    # Add service account and secrets configuration if not present
    if "serviceAccount:" not in content:
        content = f"""# Service account to use for builds
serviceAccount: 'projects/$PROJECT_ID/serviceAccounts/automation-sa-yourl@$PROJECT_ID.iam.gserviceaccount.com'
options:
  logging: CLOUD_LOGGING_ONLY
  env:
    - 'GOOGLE_CLOUD_PROJECT=$PROJECT_ID'
    
{content}"""
    
    with open(cloudbuild_path, "w") as f:
        f.write(content)
    print("\nUpdated cloudbuild.yaml with service account configuration")

def main():
    if len(sys.argv) < 2:
        print("Usage: python setup_secrets.py PROJECT_ID [SERVICE_ACCOUNT_ID]")
        sys.exit(1)
    
    project_id = sys.argv[1]
    service_account_id = sys.argv[2] if len(sys.argv) > 2 else "automation-sa-yourl"
    
    # List of secrets to create
    secrets = [
        "SENDGRID_API_KEY",
        "SSH_PRIVATE_KEY",
        "SSL_PRIVATE_KEY"
    ]
    
    setup_secret_manager(project_id, service_account_id)
    setup_secrets(project_id, service_account_id, secrets)
    update_cloudbuild_yaml()
    
    print("\n=== Setup Complete ===")
    print("\nNext steps:")
    print("1. Store your secrets using the secret_manager.py utility:")
    print("   python secret_manager.py --project PROJECT_ID --action create --secret-id SECRET_ID --value-file path/to/secret.txt")
    print("\n2. Update your application code to use the SecretManager class:")
    print("   from secret_manager import get_secret")
    print("   api_key = get_secret('SENDGRID_API_KEY')")
    print("\n3. Deploy your changes and verify the secrets are accessible")

if __name__ == "__main__":
    main()
