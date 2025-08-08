#!/usr/bin/env python3
"""
Cloud SQL Database Client for Yourl.Cloud Marketing Codes
Handles persistent storage of code history, usage logs, and authorization records
Uses secure connection manager for Secret Manager-based credentials
"""

import os
import json
import psycopg2
from datetime import datetime, timezone
from typing import Dict, Optional, Any, List
from psycopg2.extras import RealDictCursor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseClient:
    def __init__(self, project_id: str = None, connection_string: str = None):
        """
        Initialize database client with either project_id (for Secret Manager) or connection_string
        """
        self.project_id = project_id or os.environ.get('GOOGLE_CLOUD_PROJECT', 'yourl-cloud')
        self.connection_string = connection_string
        self._ensure_tables()
    
    def _get_connection(self):
        """Get a database connection using secure credentials"""
        try:
            if self.connection_string:
                # Use provided connection string (for backward compatibility)
                conn = psycopg2.connect(self.connection_string)
            else:
                # Use Secret Manager for credentials
                from scripts.database_connection_manager import DatabaseConnectionManager
                connection_manager = DatabaseConnectionManager(self.project_id)
                connection_string = connection_manager.get_connection_string()
                
                if not connection_string:
                    logger.error("Failed to get connection string from Secret Manager")
                    return None
                
                conn = psycopg2.connect(connection_string)
            
            return conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            return None
    
    def _ensure_tables(self):
        """Ensure all required tables exist"""
        conn = self._get_connection()
        if not conn:
            return
        
        try:
            with conn.cursor() as cursor:
                # Current and next marketing codes table (primary storage)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS marketing_codes (
                        id SERIAL PRIMARY KEY,
                        code_type VARCHAR(20) UNIQUE NOT NULL, -- 'current', 'next'
                        code VARCHAR(50) NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        commit_hash VARCHAR(50),
                        deployment_id VARCHAR(100),
                        rotation_reason VARCHAR(200)
                    )
                """)
                
                # Marketing code history table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS marketing_code_history (
                        id SERIAL PRIMARY KEY,
                        code VARCHAR(50) NOT NULL,
                        code_type VARCHAR(20) NOT NULL, -- 'current', 'next', 'archived'
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        deployed_at TIMESTAMP WITH TIME ZONE,
                        commit_hash VARCHAR(50),
                        deployment_id VARCHAR(100),
                        rotation_reason VARCHAR(200)
                    )
                """)
                
                # Usage logs table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS code_usage_logs (
                        id SERIAL PRIMARY KEY,
                        code VARCHAR(50) NOT NULL,
                        user_agent TEXT,
                        ip_address INET,
                        endpoint VARCHAR(100),
                        success BOOLEAN NOT NULL,
                        timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        session_id VARCHAR(100),
                        device_type VARCHAR(20)
                    )
                """)
                
                # Authorization records table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS authorization_records (
                        id SERIAL PRIMARY KEY,
                        service_name VARCHAR(100) NOT NULL,
                        service_type VARCHAR(50) NOT NULL, -- 'backend', 'frontend', 'api'
                        owner VARCHAR(100) NOT NULL,
                        code VARCHAR(50) NOT NULL,
                        access_level VARCHAR(50) NOT NULL, -- 'read', 'write', 'admin'
                        expires_at TIMESTAMP WITH TIME ZONE,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        status VARCHAR(20) DEFAULT 'active', -- 'active', 'revoked', 'expired'
                        revoked_at TIMESTAMP WITH TIME ZONE,
                        revoked_reason VARCHAR(200)
                    )
                """)
                
                # Partner onboarding table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS partner_onboarding (
                        id SERIAL PRIMARY KEY,
                        partner_name VARCHAR(100) NOT NULL,
                        partner_type VARCHAR(50) NOT NULL,
                        contact_email VARCHAR(200),
                        api_key VARCHAR(100),
                        onboarding_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
                        approved_by VARCHAR(100),
                        approved_at TIMESTAMP WITH TIME ZONE,
                        notes TEXT
                    )
                """)
                
                # Visitor tracking table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS visitor_tracking (
                        id SERIAL PRIMARY KEY,
                        visitor_id VARCHAR(100) UNIQUE NOT NULL,
                        public_tracking_key VARCHAR(50) UNIQUE NOT NULL,
                        first_visit_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        last_visit_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        last_access_code VARCHAR(50),
                        total_visits INTEGER DEFAULT 1,
                        device_type VARCHAR(20),
                        user_agent TEXT,
                        ip_address INET,
                        status VARCHAR(20) DEFAULT 'active' -- 'active', 'inactive', 'blocked'
                    )
                """)
                
                # Visitor access history table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS visitor_access_history (
                        id SERIAL PRIMARY KEY,
                        visitor_id VARCHAR(100) NOT NULL,
                        access_code VARCHAR(50) NOT NULL,
                        access_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        success BOOLEAN NOT NULL,
                        ip_address INET,
                        user_agent TEXT,
                        session_id VARCHAR(100),
                        FOREIGN KEY (visitor_id) REFERENCES visitor_tracking(visitor_id)
                    )
                """)
                
                # Landing page versions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS landing_page_versions (
                        id SERIAL PRIMARY KEY,
                        visitor_id VARCHAR(100) NOT NULL,
                        landing_page_url VARCHAR(500) NOT NULL,
                        build_version VARCHAR(100),
                        marketing_code VARCHAR(50),
                        first_accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        last_accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        access_count INTEGER DEFAULT 1
                    )
                """)
                
                conn.commit()
                logger.info("Database tables ensured successfully")
                
        except Exception as e:
            logger.error(f"Error ensuring tables: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    # Marketing Code Management Methods
    def get_current_marketing_code(self) -> Optional[str]:
        """Get the current live marketing code from database"""
        conn = self._get_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT code FROM marketing_codes 
                    WHERE code_type = 'current' 
                    ORDER BY updated_at DESC 
                    LIMIT 1
                """)
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting current marketing code: {e}")
            return None
        finally:
            conn.close()
    
    def get_next_marketing_code(self) -> Optional[str]:
        """Get the next marketing code from database"""
        conn = self._get_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT code FROM marketing_codes 
                    WHERE code_type = 'next' 
                    ORDER BY updated_at DESC 
                    LIMIT 1
                """)
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting next marketing code: {e}")
            return None
        finally:
            conn.close()
    
    def set_current_marketing_code(self, code: str, commit_hash: Optional[str] = None, 
                                  deployment_id: Optional[str] = None, 
                                  rotation_reason: Optional[str] = None) -> bool:
        """Set the current marketing code in database"""
        conn = self._get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                # Archive current code if it exists
                current_code = self.get_current_marketing_code()
                if current_code:
                    self._archive_code(current_code, 'current')
                
                # Insert or update current code
                cursor.execute("""
                    INSERT INTO marketing_codes (code_type, code, commit_hash, deployment_id, rotation_reason, updated_at)
                    VALUES ('current', %s, %s, %s, %s, %s)
                    ON CONFLICT (code_type) 
                    DO UPDATE SET 
                        code = EXCLUDED.code,
                        commit_hash = EXCLUDED.commit_hash,
                        deployment_id = EXCLUDED.deployment_id,
                        rotation_reason = EXCLUDED.rotation_reason,
                        updated_at = EXCLUDED.updated_at
                """, (code, commit_hash, deployment_id, rotation_reason, datetime.now(timezone.utc)))
                
                # Add to history
                self._add_to_history(code, 'current', commit_hash, deployment_id, rotation_reason)
                
                conn.commit()
                logger.info(f"Set current marketing code: {code}")
                return True
        except Exception as e:
            logger.error(f"Error setting current marketing code: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def set_next_marketing_code(self, code: str, commit_hash: Optional[str] = None, 
                               deployment_id: Optional[str] = None, 
                               rotation_reason: Optional[str] = None) -> bool:
        """Set the next marketing code in database"""
        conn = self._get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                # Archive next code if it exists
                next_code = self.get_next_marketing_code()
                if next_code:
                    self._archive_code(next_code, 'next')
                
                # Insert or update next code
                cursor.execute("""
                    INSERT INTO marketing_codes (code_type, code, commit_hash, deployment_id, rotation_reason, updated_at)
                    VALUES ('next', %s, %s, %s, %s, %s)
                    ON CONFLICT (code_type) 
                    DO UPDATE SET 
                        code = EXCLUDED.code,
                        commit_hash = EXCLUDED.commit_hash,
                        deployment_id = EXCLUDED.deployment_id,
                        rotation_reason = EXCLUDED.rotation_reason,
                        updated_at = EXCLUDED.updated_at
                """, (code, commit_hash, deployment_id, rotation_reason, datetime.now(timezone.utc)))
                
                # Add to history
                self._add_to_history(code, 'next', commit_hash, deployment_id, rotation_reason)
                
                conn.commit()
                logger.info(f"Set next marketing code: {code}")
                return True
        except Exception as e:
            logger.error(f"Error setting next marketing code: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def rotate_codes(self, new_current_code: str, new_next_code: str, 
                    commit_hash: Optional[str] = None, deployment_id: Optional[str] = None) -> bool:
        """Rotate codes: current becomes archived, next becomes current, new next is set"""
        try:
            # Archive current code
            current_code = self.get_current_marketing_code()
            if current_code:
                self._archive_code(current_code, 'current')
            
            # Archive next code
            next_code = self.get_next_marketing_code()
            if next_code:
                self._archive_code(next_code, 'next')
            
            # Set new codes
            success1 = self.set_current_marketing_code(new_current_code, commit_hash, deployment_id, "rotation")
            success2 = self.set_next_marketing_code(new_next_code, commit_hash, deployment_id, "rotation")
            
            return success1 and success2
        except Exception as e:
            logger.error(f"Error rotating codes: {e}")
            return False
    
    def _archive_code(self, code: str, code_type: str):
        """Archive a code in history"""
        self._add_to_history(code, f'archived_{code_type}')
    
    def _add_to_history(self, code: str, code_type: str, commit_hash: Optional[str] = None, 
                       deployment_id: Optional[str] = None, rotation_reason: Optional[str] = None):
        """Add a code to history"""
        conn = self._get_connection()
        if not conn:
            return
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO marketing_code_history 
                    (code, code_type, commit_hash, deployment_id, rotation_reason, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (code, code_type, commit_hash, deployment_id, rotation_reason, datetime.now(timezone.utc)))
                
                conn.commit()
        except Exception as e:
            logger.error(f"Error adding to history: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def get_code_metadata(self) -> Dict[str, Any]:
        """Get metadata about the marketing codes"""
        conn = self._get_connection()
        if not conn:
            return {}
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Get current and next codes
                cursor.execute("""
                    SELECT code_type, code, updated_at, commit_hash, deployment_id
                    FROM marketing_codes 
                    ORDER BY code_type, updated_at DESC
                """)
                codes = [dict(row) for row in cursor.fetchall()]
                
                # Get history count
                cursor.execute("SELECT COUNT(*) as history_count FROM marketing_code_history")
                history_result = cursor.fetchone()
                history_count = history_result['history_count'] if history_result else 0
                
                return {
                    'current_code_exists': any(c['code_type'] == 'current' for c in codes),
                    'next_code_exists': any(c['code_type'] == 'next' for c in codes),
                    'codes': codes,
                    'history_count': history_count,
                    'last_updated': max([c['updated_at'] for c in codes]) if codes else None
                }
        except Exception as e:
            logger.error(f"Error getting code metadata: {e}")
            return {}
        finally:
            conn.close()
    
    def log_code_history(self, code: str, code_type: str, commit_hash: Optional[str] = None, 
                        deployment_id: Optional[str] = None, rotation_reason: Optional[str] = None) -> bool:
        """Log a marketing code change"""
        return self._add_to_history(code, code_type, commit_hash, deployment_id, rotation_reason) is not None
    
    def log_usage(self, code: str, user_agent: Optional[str] = None, ip_address: Optional[str] = None,
                  endpoint: Optional[str] = None, success: bool = True, session_id: Optional[str] = None,
                  device_type: Optional[str] = None) -> bool:
        """Log code usage"""
        conn = self._get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO code_usage_logs 
                    (code, user_agent, ip_address, endpoint, success, session_id, device_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (code, user_agent, ip_address, endpoint, success, session_id, device_type))
                
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error logging usage: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def create_authorization_record(self, service_name: str, service_type: str, owner: str,
                                  code: str, access_level: str, expires_at: Optional[datetime] = None) -> bool:
        """Create a new authorization record"""
        conn = self._get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO authorization_records 
                    (service_name, service_type, owner, code, access_level, expires_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (service_name, service_type, owner, code, access_level, expires_at))
                
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error creating authorization record: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def revoke_authorization(self, service_name: str, reason: Optional[str] = None) -> bool:
        """Revoke authorization for a service"""
        conn = self._get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE authorization_records 
                    SET status = 'revoked', revoked_at = %s, revoked_reason = %s
                    WHERE service_name = %s AND status = 'active'
                """, (datetime.now(timezone.utc), reason, service_name))
                
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error revoking authorization: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_code_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get marketing code history"""
        conn = self._get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM marketing_code_history 
                    ORDER BY created_at DESC 
                    LIMIT %s
                """, (limit,))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting code history: {e}")
            return []
        finally:
            conn.close()
    
    def get_usage_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get usage statistics"""
        conn = self._get_connection()
        if not conn:
            return {}
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Total usage
                cursor.execute("""
                    SELECT COUNT(*) as total_usage,
                           COUNT(CASE WHEN success = true THEN 1 END) as successful_usage,
                           COUNT(CASE WHEN success = false THEN 1 END) as failed_usage
                    FROM code_usage_logs 
                    WHERE timestamp >= NOW() - INTERVAL '%s days'
                """, (days,))
                
                usage_stats = cursor.fetchone()
                
                # Usage by code
                cursor.execute("""
                    SELECT code, COUNT(*) as usage_count
                    FROM code_usage_logs 
                    WHERE timestamp >= NOW() - INTERVAL '%s days'
                    GROUP BY code
                    ORDER BY usage_count DESC
                """, (days,))
                
                usage_by_code = [dict(row) for row in cursor.fetchall()]
                
                if usage_stats:
                    return {
                        "period_days": days,
                        "total_usage": usage_stats['total_usage'],
                        "successful_usage": usage_stats['successful_usage'],
                        "failed_usage": usage_stats['failed_usage'],
                        "usage_by_code": usage_by_code
                    }
                else:
                    return {
                        "period_days": days,
                        "total_usage": 0,
                        "successful_usage": 0,
                        "failed_usage": 0,
                        "usage_by_code": usage_by_code
                    }
        except Exception as e:
            logger.error(f"Error getting usage stats: {e}")
            return {}
        finally:
            conn.close()
    
    def get_active_authorizations(self) -> List[Dict[str, Any]]:
        """Get all active authorizations"""
        conn = self._get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM authorization_records 
                    WHERE status = 'active' AND (expires_at IS NULL OR expires_at > NOW())
                    ORDER BY created_at DESC
                """)
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting active authorizations: {e}")
            return []
        finally:
            conn.close()
    
    def get_or_create_visitor(self, visitor_id: str, user_agent: Optional[str] = None, 
                             ip_address: Optional[str] = None, device_type: Optional[str] = None) -> Dict[str, Any]:
        """Get or create a visitor record"""
        conn = self._get_connection()
        if not conn:
            return {}
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Check if visitor exists
                cursor.execute("""
                    SELECT * FROM visitor_tracking 
                    WHERE visitor_id = %s
                """, (visitor_id,))
                
                visitor = cursor.fetchone()
                
                if visitor:
                    # Update last visit
                    cursor.execute("""
                        UPDATE visitor_tracking 
                        SET last_visit_at = NOW(), total_visits = total_visits + 1,
                            user_agent = %s, ip_address = %s, device_type = %s
                        WHERE visitor_id = %s
                    """, (user_agent, ip_address, device_type, visitor_id))
                    
                    conn.commit()
                    return dict(visitor)
                else:
                    # Create new visitor
                    import random
                    import string
                    
                    # Generate unique tracking key
                    tracking_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                    
                    cursor.execute("""
                        INSERT INTO visitor_tracking 
                        (visitor_id, public_tracking_key, user_agent, ip_address, device_type)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING *
                    """, (visitor_id, tracking_key, user_agent, ip_address, device_type))
                    
                    new_visitor = cursor.fetchone()
                    conn.commit()
                    return dict(new_visitor) if new_visitor else {}
                    
        except Exception as e:
            logger.error(f"Error getting/creating visitor: {e}")
            conn.rollback()
            return {}
        finally:
            conn.close()
    
    def log_visitor_access(self, visitor_id: str, access_code: str, success: bool,
                          user_agent: Optional[str] = None, ip_address: Optional[str] = None,
                          session_id: Optional[str] = None) -> bool:
        """Log visitor access attempt"""
        conn = self._get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                # Log access history
                cursor.execute("""
                    INSERT INTO visitor_access_history 
                    (visitor_id, access_code, success, ip_address, user_agent, session_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (visitor_id, access_code, success, ip_address, user_agent, session_id))
                
                # Update visitor's last access code if successful
                if success:
                    cursor.execute("""
                        UPDATE visitor_tracking 
                        SET last_access_code = %s
                        WHERE visitor_id = %s
                    """, (access_code, visitor_id))
                
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error logging visitor access: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_visitor_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get visitor statistics"""
        conn = self._get_connection()
        if not conn:
            return {}
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Total visitors
                cursor.execute("""
                    SELECT COUNT(*) as total_visitors,
                           COUNT(CASE WHEN last_visit_at >= NOW() - INTERVAL '%s days' THEN 1 END) as active_visitors
                    FROM visitor_tracking
                """, (days,))
                
                visitor_stats = cursor.fetchone()
                
                # Access attempts
                cursor.execute("""
                    SELECT COUNT(*) as total_attempts,
                           COUNT(CASE WHEN success = true THEN 1 END) as successful_attempts,
                           COUNT(CASE WHEN success = false THEN 1 END) as failed_attempts
                    FROM visitor_access_history 
                    WHERE access_timestamp >= NOW() - INTERVAL '%s days'
                """, (days,))
                
                access_stats = cursor.fetchone()
                
                if visitor_stats and access_stats:
                    return {
                        "period_days": days,
                        "total_visitors": visitor_stats['total_visitors'],
                        "active_visitors": visitor_stats['active_visitors'],
                        "total_access_attempts": access_stats['total_attempts'],
                        "successful_attempts": access_stats['successful_attempts'],
                        "failed_attempts": access_stats['failed_attempts']
                    }
                else:
                    return {
                        "period_days": days,
                        "total_visitors": 0,
                        "active_visitors": 0,
                        "total_access_attempts": 0,
                        "successful_attempts": 0,
                        "failed_attempts": 0
                    }
        except Exception as e:
            logger.error(f"Error getting visitor stats: {e}")
            return {}
        finally:
            conn.close()
    
    def store_landing_page_version(self, visitor_id: str, landing_page_url: str, 
                                  build_version: Optional[str] = None, 
                                  marketing_code: Optional[str] = None) -> bool:
        """Store or update landing page version for a visitor"""
        conn = self._get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                # Check if visitor already has a landing page version record
                cursor.execute("""
                    SELECT id, access_count FROM landing_page_versions 
                    WHERE visitor_id = %s
                """, (visitor_id,))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing record
                    cursor.execute("""
                        UPDATE landing_page_versions 
                        SET landing_page_url = %s, build_version = %s, marketing_code = %s,
                            last_accessed_at = NOW(), access_count = access_count + 1
                        WHERE visitor_id = %s
                    """, (landing_page_url, build_version, marketing_code, visitor_id))
                else:
                    # Create new record
                    cursor.execute("""
                        INSERT INTO landing_page_versions 
                        (visitor_id, landing_page_url, build_version, marketing_code)
                        VALUES (%s, %s, %s, %s)
                    """, (visitor_id, landing_page_url, build_version, marketing_code))
                
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error storing landing page version: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_landing_page_version(self, visitor_id: str) -> Optional[Dict[str, Any]]:
        """Get the landing page version for a visitor"""
        conn = self._get_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM landing_page_versions 
                    WHERE visitor_id = %s
                    ORDER BY last_accessed_at DESC
                    LIMIT 1
                """, (visitor_id,))
                result = cursor.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logger.error(f"Error getting landing page version: {e}")
            return None
        finally:
            conn.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database Client")
    parser.add_argument("--connection-string", required=True, help="Database connection string")
    parser.add_argument("--action", choices=['log-history', 'log-usage', 'create-auth', 'revoke-auth', 'get-history', 'get-stats', 'get-auths'],
                       required=True, help="Action to perform")
    parser.add_argument("--code", help="Marketing code")
    parser.add_argument("--code-type", help="Code type (current, next, archived)")
    parser.add_argument("--service-name", help="Service name")
    parser.add_argument("--owner", help="Owner")
    parser.add_argument("--access-level", help="Access level")
    parser.add_argument("--days", type=int, default=30, help="Days for stats")
    
    args = parser.parse_args()
    
    client = DatabaseClient(args.connection_string)
    
    if args.action == 'log-history':
        if not all([args.code, args.code_type]):
            parser.error("--code and --code-type required for log-history action")
        success = client.log_code_history(args.code, args.code_type)
        print(f"Logged code history: {'Success' if success else 'Failed'}")
        
    elif args.action == 'log-usage':
        if not args.code:
            parser.error("--code required for log-usage action")
        success = client.log_usage(args.code)
        print(f"Logged usage: {'Success' if success else 'Failed'}")
        
    elif args.action == 'create-auth':
        if not all([args.service_name, args.owner, args.code, args.access_level]):
            parser.error("--service-name, --owner, --code, and --access-level required for create-auth action")
        success = client.create_authorization_record(args.service_name, "api", args.owner, args.code, args.access_level)
        print(f"Created authorization: {'Success' if success else 'Failed'}")
        
    elif args.action == 'revoke-auth':
        if not args.service_name:
            parser.error("--service-name required for revoke-auth action")
        success = client.revoke_authorization(args.service_name)
        print(f"Revoked authorization: {'Success' if success else 'Failed'}")
        
    elif args.action == 'get-history':
        history = client.get_code_history()
        print(json.dumps(history, indent=2, default=str))
        
    elif args.action == 'get-stats':
        stats = client.get_usage_stats(args.days)
        print(json.dumps(stats, indent=2, default=str))
        
    elif args.action == 'get-auths':
        auths = client.get_active_authorizations()
        print(json.dumps(auths, indent=2, default=str))
