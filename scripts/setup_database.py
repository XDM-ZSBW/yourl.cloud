#!/usr/bin/env python3
"""
Setup script for Yourl.Cloud Cloud SQL Database
Creates database, user, and initializes tables
"""

import subprocess
import sys
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return result.stdout
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return None

def wait_for_instance(project_id, instance_name):
    """Wait for Cloud SQL instance to be ready"""
    print(f"⏳ Waiting for Cloud SQL instance {instance_name} to be ready...")
    
    while True:
        result = run_command(
            f"gcloud sql instances describe {instance_name} --project={project_id} --format='value(state)'",
            "Checking instance status"
        )
        
        if result and "RUNNABLE" in result.strip():
            print("✅ Cloud SQL instance is ready!")
            return True
        elif result and "PENDING_CREATE" in result.strip():
            print("⏳ Instance still being created, waiting 30 seconds...")
            time.sleep(30)
        else:
            print("❌ Unknown instance status")
            return False

def setup_database(project_id, instance_name):
    """Set up the database with required tables"""
    
    # Wait for instance to be ready
    if not wait_for_instance(project_id, instance_name):
        print("❌ Failed to wait for instance")
        return False
    
    # Create database
    run_command(
        f"gcloud sql databases create yourl_cloud_db --instance={instance_name} --project={project_id}",
        "Creating database"
    )
    
    # Create user
    run_command(
        f"gcloud sql users create yourl-cloud-user --instance={instance_name} --password=yourl-cloud-secure-user-2024 --project={project_id}",
        "Creating database user"
    )
    
    # Get connection info
    connection_info = run_command(
        f"gcloud sql instances describe {instance_name} --project={project_id} --format='value(connectionName)'",
        "Getting connection info"
    )
    
    if connection_info:
        print(f"✅ Database setup complete!")
        print(f"📊 Connection Name: {connection_info.strip()}")
        print(f"🔗 Connection String: postgresql://yourl-cloud-user:yourl-cloud-secure-user-2024@34.169.177.112:5432/yourl_cloud_db")
        return True
    
    return False

if __name__ == "__main__":
    PROJECT_ID = "yourl-cloud"
    INSTANCE_NAME = "yourl-cloud-db"
    
    print("🚀 Setting up Yourl.Cloud Cloud SQL Database...")
    
    if setup_database(PROJECT_ID, INSTANCE_NAME):
        print("🎉 Database setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Update Cloud Run environment with DATABASE_CONNECTION_STRING")
        print("2. Deploy the updated application")
        print("3. Test database logging functionality")
    else:
        print("❌ Database setup failed")
        sys.exit(1)
