#!/usr/bin/env python3
"""
Migration script to transition marketing codes from Secret Manager to database storage
"""

import os
import sys
import argparse
from datetime import datetime, timezone
from typing import Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.secret_manager_client import SecretManagerClient
from scripts.database_client import DatabaseClient

def migrate_codes_to_database(project_id: str, database_connection_string: str) -> bool:
    """
    Migrate marketing codes from Secret Manager to database
    """
    print(f"🔄 Starting migration from Secret Manager to database...")
    print(f"Project ID: {project_id}")
    print(f"Database: {database_connection_string.split('@')[1] if '@' in database_connection_string else 'Unknown'}")
    
    try:
        # Initialize clients
        secret_client = SecretManagerClient(project_id)
        db_client = DatabaseClient(database_connection_string)
        
        # Get current codes from Secret Manager
        print("\n📥 Retrieving codes from Secret Manager...")
        current_code = secret_client.get_current_marketing_code()
        next_code = secret_client.get_next_marketing_code()
        
        if current_code:
            print(f"✅ Found current code: {current_code}")
        else:
            print("⚠️ No current code found in Secret Manager")
        
        if next_code:
            print(f"✅ Found next code: {next_code}")
        else:
            print("⚠️ No next code found in Secret Manager")
        
        # Migrate to database
        print("\n📤 Migrating codes to database...")
        
        if current_code:
            success = db_client.set_current_marketing_code(
                current_code, 
                rotation_reason="migration_from_secret_manager"
            )
            if success:
                print(f"✅ Migrated current code to database: {current_code}")
            else:
                print(f"❌ Failed to migrate current code: {current_code}")
                return False
        
        if next_code:
            success = db_client.set_next_marketing_code(
                next_code, 
                rotation_reason="migration_from_secret_manager"
            )
            if success:
                print(f"✅ Migrated next code to database: {next_code}")
            else:
                print(f"❌ Failed to migrate next code: {next_code}")
                return False
        
        # Verify migration
        print("\n🔍 Verifying migration...")
        db_current = db_client.get_current_marketing_code()
        db_next = db_client.get_next_marketing_code()
        
        if db_current == current_code:
            print(f"✅ Current code verified: {db_current}")
        else:
            print(f"❌ Current code mismatch: expected {current_code}, got {db_current}")
            return False
        
        if db_next == next_code:
            print(f"✅ Next code verified: {db_next}")
        else:
            print(f"❌ Next code mismatch: expected {next_code}, got {db_next}")
            return False
        
        # Get metadata
        metadata = db_client.get_code_metadata()
        print(f"\n📊 Migration summary:")
        print(f"   Current code exists: {metadata.get('current_code_exists', False)}")
        print(f"   Next code exists: {metadata.get('next_code_exists', False)}")
        print(f"   History count: {metadata.get('history_count', 0)}")
        print(f"   Last updated: {metadata.get('last_updated', 'Unknown')}")
        
        print(f"\n🎉 Migration completed successfully!")
        print(f"💡 You can now remove Secret Manager dependencies and use database storage exclusively.")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def verify_database_storage(database_connection_string: str) -> bool:
    """
    Verify that database storage is working correctly
    """
    print(f"🔍 Verifying database storage...")
    
    try:
        db_client = DatabaseClient(database_connection_string)
        
        # Test current code
        current_code = db_client.get_current_marketing_code()
        if current_code:
            print(f"✅ Current code retrieved: {current_code}")
        else:
            print("⚠️ No current code found in database")
        
        # Test next code
        next_code = db_client.get_next_marketing_code()
        if next_code:
            print(f"✅ Next code retrieved: {next_code}")
        else:
            print("⚠️ No next code found in database")
        
        # Get metadata
        metadata = db_client.get_code_metadata()
        print(f"\n📊 Database status:")
        print(f"   Current code exists: {metadata.get('current_code_exists', False)}")
        print(f"   Next code exists: {metadata.get('next_code_exists', False)}")
        print(f"   History count: {metadata.get('history_count', 0)}")
        print(f"   Last updated: {metadata.get('last_updated', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Migrate marketing codes from Secret Manager to database")
    parser.add_argument("--project-id", required=True, help="Google Cloud project ID")
    parser.add_argument("--database-connection-string", required=True, help="Database connection string")
    parser.add_argument("--action", choices=['migrate', 'verify'], default='migrate', 
                       help="Action to perform (migrate or verify)")
    
    args = parser.parse_args()
    
    if args.action == 'migrate':
        success = migrate_codes_to_database(args.project_id, args.database_connection_string)
        sys.exit(0 if success else 1)
    elif args.action == 'verify':
        success = verify_database_storage(args.database_connection_string)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
