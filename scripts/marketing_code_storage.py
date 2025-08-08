#!/usr/bin/env python3
"""
Cost-Effective Marketing Code Storage for Yourl.Cloud
Uses local file storage instead of expensive Secret Manager for marketing codes
"""

import os
import json
import hashlib
import shutil
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketingCodeStorage:
    def __init__(self, project_id: str, storage_dir: str = "codes"):
        self.project_id = project_id
        self.storage_dir = storage_dir
        self.codes_file = os.path.join(storage_dir, "marketing_codes.json")
        self.backup_dir = os.path.join(storage_dir, "backups")
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure storage and backup directories exist"""
        os.makedirs(self.storage_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def _load_codes(self) -> Dict[str, Any]:
        """Load codes from file"""
        try:
            if os.path.exists(self.codes_file):
                with open(self.codes_file, 'r') as f:
                    return json.load(f)
            else:
                return {
                    'current_code': '',
                    'next_code': '',
                    'code_history': [],
                    'last_updated': datetime.now(timezone.utc).isoformat(),
                    'project_id': self.project_id
                }
        except Exception as e:
            logger.error(f"Error loading codes: {e}")
            return {
                'current_code': '',
                'next_code': '',
                'code_history': [],
                'last_updated': datetime.now(timezone.utc).isoformat(),
                'project_id': self.project_id
            }
    
    def _save_codes(self, codes_data: Dict[str, Any]) -> bool:
        """Save codes to file with backup"""
        try:
            # Create backup before saving
            if os.path.exists(self.codes_file):
                backup_file = os.path.join(
                    self.backup_dir, 
                    f"marketing_codes_backup_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
                )
                shutil.copy2(self.codes_file, backup_file)
                logger.info(f"Created backup: {backup_file}")
            
            # Update timestamp
            codes_data['last_updated'] = datetime.now(timezone.utc).isoformat()
            
            # Save to file
            with open(self.codes_file, 'w') as f:
                json.dump(codes_data, f, indent=2)
            
            logger.info(f"Saved codes to {self.codes_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving codes: {e}")
            return False
    
    def get_current_marketing_code(self) -> Optional[str]:
        """Get the current live marketing code"""
        codes_data = self._load_codes()
        return codes_data.get('current_code')
    
    def get_next_marketing_code(self) -> Optional[str]:
        """Get the next marketing code"""
        codes_data = self._load_codes()
        return codes_data.get('next_code')
    
    def set_current_marketing_code(self, code: str) -> bool:
        """Set the current marketing code"""
        codes_data = self._load_codes()
        
        # Archive current code if it exists
        if codes_data.get('current_code'):
            self._archive_code(codes_data['current_code'], 'current')
        
        # Set new current code
        codes_data['current_code'] = code
        
        # Add to history
        self._add_to_history(code, 'current')
        
        return self._save_codes(codes_data)
    
    def set_next_marketing_code(self, code: str) -> bool:
        """Set the next marketing code"""
        codes_data = self._load_codes()
        
        # Archive next code if it exists
        if codes_data.get('next_code'):
            self._archive_code(codes_data['next_code'], 'next')
        
        # Set new next code
        codes_data['next_code'] = code
        
        # Add to history
        self._add_to_history(code, 'next')
        
        return self._save_codes(codes_data)
    
    def rotate_codes(self, new_current_code: str, new_next_code: str) -> bool:
        """Rotate codes: current becomes archived, next becomes current, new next is set"""
        try:
            codes_data = self._load_codes()
            
            # Archive current code
            if codes_data.get('current_code'):
                self._archive_code(codes_data['current_code'], 'current')
            
            # Archive next code
            if codes_data.get('next_code'):
                self._archive_code(codes_data['next_code'], 'next')
            
            # Set new codes
            codes_data['current_code'] = new_current_code
            codes_data['next_code'] = new_next_code
            
            # Add to history
            self._add_to_history(new_current_code, 'current')
            self._add_to_history(new_next_code, 'next')
            
            return self._save_codes(codes_data)
        except Exception as e:
            logger.error(f"Error rotating codes: {e}")
            return False
    
    def _archive_code(self, code: str, code_type: str):
        """Archive a code in history"""
        codes_data = self._load_codes()
        
        archive_entry = {
            'code': code,
            'type': f'archived_{code_type}',
            'archived_at': datetime.now(timezone.utc).isoformat(),
            'project_id': self.project_id
        }
        
        codes_data['code_history'].append(archive_entry)
    
    def _add_to_history(self, code: str, code_type: str):
        """Add a code to history"""
        codes_data = self._load_codes()
        
        history_entry = {
            'code': code,
            'type': code_type,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'project_id': self.project_id
        }
        
        codes_data['code_history'].append(history_entry)
    
    def get_code_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get marketing code history"""
        codes_data = self._load_codes()
        history = codes_data.get('code_history', [])
        return history[-limit:] if limit else history
    
    def get_code_metadata(self) -> Dict[str, Any]:
        """Get metadata about the code storage"""
        codes_data = self._load_codes()
        return {
            'project_id': codes_data.get('project_id'),
            'last_updated': codes_data.get('last_updated'),
            'current_code_exists': bool(codes_data.get('current_code')),
            'next_code_exists': bool(codes_data.get('next_code')),
            'history_count': len(codes_data.get('code_history', [])),
            'storage_location': os.path.abspath(self.codes_file),
            'backup_location': os.path.abspath(self.backup_dir)
        }
    
    def cleanup_old_backups(self, keep_days: int = 30) -> int:
        """Clean up old backup files"""
        try:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=keep_days)
            deleted_count = 0
            
            for filename in os.listdir(self.backup_dir):
                if filename.startswith('marketing_codes_backup_'):
                    file_path = os.path.join(self.backup_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path), tz=timezone.utc)
                    
                    if file_time < cutoff_date:
                        os.remove(file_path)
                        deleted_count += 1
                        logger.info(f"Deleted old backup: {filename}")
            
            return deleted_count
        except Exception as e:
            logger.error(f"Error cleaning up backups: {e}")
            return 0
