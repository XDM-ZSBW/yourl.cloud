#!/usr/bin/env python3
"""
Secure Database Connection Manager for Yourl.Cloud
Uses Google Secret Manager to store database credentials securely
"""

import os
import json
from typing import Optional, Dict, Any
from google.cloud import secretmanager
from google.api_core import exceptions
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnectionManager:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()
        
        # Secret names for database credentials
        self.db_host_secret = f"projects/{project_id}/secrets/yourl_db_host"
        self.db_port_secret = f"projects/{project_id}/secrets/yourl_db_port"
        self.db_name_secret = f"projects/{project_id}/secrets/yourl_db_name"
        self.db_user_secret = f"projects/{project_id}/secrets/yourl_db_user"
        self.db_password_secret = f"projects/{project_id}/secrets/yourl_db_password"
        
    def _get_secret(self, secret_name: str, version: str = "latest") -> Optional[str]:
        """Get a secret value from Secret Manager"""
        try:
            name = f"{secret_name}/versions/{version}"
            response = self.client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except exceptions.NotFound:
            logger.warning(f"Secret {secret_name} not found")
            return None
        except Exception as e:
            logger.error(f"Error accessing secret {secret_name}: {e}")
            return None
    
    def get_connection_string(self) -> Optional[str]:
        """Build database connection string from Secret Manager credentials"""
        try:
            # Get all database credentials from Secret Manager
            host = self._get_secret(self.db_host_secret)
            port = self._get_secret(self.db_port_secret) or "5432"
            database = self._get_secret(self.db_name_secret)
            user = self._get_secret(self.db_user_secret)
            password = self._get_secret(self.db_password_secret)
            
            # Validate required credentials
            if not all([host, database, user, password]):
                logger.error("Missing required database credentials in Secret Manager")
                return None
            
            # Build connection string
            connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
            logger.info(f"Successfully built database connection string for {user}@{host}:{port}/{database}")
            return connection_string
            
        except Exception as e:
            logger.error(f"Error building connection string: {e}")
            return None
    
    def get_connection_params(self) -> Optional[Dict[str, str]]:
        """Get database connection parameters as a dictionary"""
        try:
            host = self._get_secret(self.db_host_secret)
            port = self._get_secret(self.db_port_secret) or "5432"
            database = self._get_secret(self.db_name_secret)
            user = self._get_secret(self.db_user_secret)
            password = self._get_secret(self.db_password_secret)
            
            # Validate required credentials
            if not all([host, database, user, password]):
                logger.error("Missing required database credentials in Secret Manager")
                return None
            
            # Ensure all values are strings
            return {
                "host": str(host),
                "port": str(port),
                "database": str(database),
                "user": str(user),
                "password": str(password)
            }
            
        except Exception as e:
            logger.error(f"Error getting connection parameters: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test database connection using credentials from Secret Manager"""
        try:
            connection_string = self.get_connection_string()
            if not connection_string:
                return False
            
            # Import psycopg2 here to avoid dependency issues
            import psycopg2
            
            conn = psycopg2.connect(connection_string)
            conn.close()
            logger.info("✅ Database connection test successful")
            return True
            
        except ImportError:
            logger.error("psycopg2 not installed - cannot test connection")
            return False
        except Exception as e:
            logger.error(f"❌ Database connection test failed: {e}")
            return False
    
    def create_secrets(self, host: str, port: str, database: str, user: str, password: str) -> bool:
        """Create database credential secrets in Secret Manager"""
        try:
            secrets_data = {
                self.db_host_secret: host,
                self.db_port_secret: port,
                self.db_name_secret: database,
                self.db_user_secret: user,
                self.db_password_secret: password
            }
            
            for secret_name, secret_value in secrets_data.items():
                # Extract secret ID from full name
                secret_id = secret_name.split('/')[-1]
                
                # Create secret if it doesn't exist
                try:
                    parent = f"projects/{self.project_id}"
                    secret = {"replication": {"automatic": {}}}
                    self.client.create_secret(request={"parent": parent, "secret_id": secret_id, "secret": secret})
                    logger.info(f"Created secret: {secret_id}")
                except exceptions.AlreadyExists:
                    logger.info(f"Secret already exists: {secret_id}")
                
                # Add secret version
                try:
                    secret_path = self.client.secret_path(self.project_id, secret_id)
                    payload = {"data": secret_value.encode("UTF-8")}
                    self.client.add_secret_version(request={"parent": secret_path, "payload": payload})
                    logger.info(f"Added version to secret: {secret_id}")
                except Exception as e:
                    logger.error(f"Error adding version to secret {secret_id}: {e}")
                    return False
            
            logger.info("✅ All database secrets created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating secrets: {e}")
            return False
    
    def list_secrets(self) -> Dict[str, bool]:
        """List all database-related secrets and their status"""
        secrets = {
            "db_host": self.db_host_secret,
            "db_port": self.db_port_secret,
            "db_name": self.db_name_secret,
            "db_user": self.db_user_secret,
            "db_password": self.db_password_secret
        }
        
        status = {}
        for name, secret_path in secrets.items():
            try:
                secret_id = secret_path.split('/')[-1]
                secret_path = self.client.secret_path(self.project_id, secret_id)
                self.client.get_secret(request={"name": secret_path})
                status[name] = True
            except exceptions.NotFound:
                status[name] = False
            except Exception as e:
                logger.error(f"Error checking secret {name}: {e}")
                status[name] = False
        
        return status

def main():
    """CLI interface for database connection manager"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Database Connection Manager")
    parser.add_argument("--project-id", required=True, help="Google Cloud project ID")
    parser.add_argument("--action", choices=['test', 'create-secrets', 'list-secrets', 'get-connection'], 
                       default='test', help="Action to perform")
    parser.add_argument("--host", help="Database host (for create-secrets)")
    parser.add_argument("--port", default="5432", help="Database port (for create-secrets)")
    parser.add_argument("--database", help="Database name (for create-secrets)")
    parser.add_argument("--user", help="Database user (for create-secrets)")
    parser.add_argument("--password", help="Database password (for create-secrets)")
    
    args = parser.parse_args()
    
    manager = DatabaseConnectionManager(args.project_id)
    
    if args.action == 'test':
        success = manager.test_connection()
        print(f"Connection test: {'✅ Success' if success else '❌ Failed'}")
        
    elif args.action == 'create-secrets':
        if not all([args.host, args.database, args.user, args.password]):
            parser.error("--host, --database, --user, and --password required for create-secrets")
        
        success = manager.create_secrets(args.host, args.port, args.database, args.user, args.password)
        print(f"Secret creation: {'✅ Success' if success else '❌ Failed'}")
        
    elif args.action == 'list-secrets':
        status = manager.list_secrets()
        print("Database secrets status:")
        for name, exists in status.items():
            print(f"  {name}: {'✅ Exists' if exists else '❌ Missing'}")
            
    elif args.action == 'get-connection':
        connection_string = manager.get_connection_string()
        if connection_string:
            # Mask password in output
            password = manager._get_secret(manager.db_password_secret)
            if password:
                masked = connection_string.replace(password, "***")
            else:
                masked = connection_string
            print(f"Connection string: {masked}")
        else:
            print("❌ Failed to get connection string")

if __name__ == "__main__":
    main()
