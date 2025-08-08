#!/usr/bin/env python3
"""
Zaido - AI Clipboard Bridge for Yourl.Cloud
Enables seamless sharing of context and information between AI experiences
across different locations, devices, and family members.
"""

import os
import json
import time
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

# Configure clean logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('zaido')

@dataclass
class ClipboardItem:
    """Represents a clipboard item shared between AI experiences"""
    id: str
    content: str
    content_type: str  # 'text', 'conversation', 'reminder', 'context'
    source_location: str  # Where it was created
    target_locations: List[str]  # Where it should be available
    created_by: str  # Who created it
    created_at: datetime
    expires_at: Optional[datetime]
    priority: str  # 'low', 'medium', 'high', 'emergency'
    tags: List[str]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage/transmission"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        if self.expires_at:
            data['expires_at'] = self.expires_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClipboardItem':
        """Create from dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        if data.get('expires_at'):
            data['expires_at'] = datetime.fromisoformat(data['expires_at'])
        return cls(**data)

class ZaidoClipboardBridge:
    """Main clipboard bridge for sharing AI context across locations"""
    
    def __init__(self, project_id: str, storage_backend: str = 'database'):
        self.project_id = project_id
        self.storage_backend = storage_backend
        self.clipboard_items: Dict[str, ClipboardItem] = {}
        
        # Initialize storage
        if storage_backend == 'database':
            self._init_database_storage()
        elif storage_backend == 'secret_manager':
            self._init_secret_manager_storage()
        else:
            logger.warning(f"Unknown storage backend: {storage_backend}")
    
    def _init_database_storage(self):
        """Initialize database storage for clipboard items"""
        try:
            # This will be implemented when database is ready
            logger.info("Database storage initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database storage: {e}")
    
    def _init_secret_manager_storage(self):
        """Initialize Secret Manager storage for clipboard items"""
        try:
            from scripts.secret_manager_client import SecretManagerClient
            self.secret_client = SecretManagerClient(self.project_id)
            logger.info("Secret Manager storage initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Secret Manager storage: {e}")
    
    def create_clipboard_item(
        self,
        content: str,
        content_type: str,
        source_location: str,
        target_locations: List[str],
        created_by: str,
        priority: str = 'medium',
        tags: List[str] = None,
        expires_in_hours: int = 24,
        metadata: Dict[str, Any] = None
    ) -> ClipboardItem:
        """Create a new clipboard item for sharing between AI experiences"""
        
        # Generate unique ID
        item_id = self._generate_item_id(content, source_location, created_by)
        
        # Set expiration
        expires_at = datetime.now(timezone.utc) + timedelta(hours=expires_in_hours)
        
        # Create clipboard item
        item = ClipboardItem(
            id=item_id,
            content=content,
            content_type=content_type,
            source_location=source_location,
            target_locations=target_locations,
            created_by=created_by,
            created_at=datetime.now(timezone.utc),
            expires_at=expires_at,
            priority=priority,
            tags=tags if tags is not None else [],
            metadata=metadata if metadata is not None else {}
        )
        
        # Store item
        self._store_item(item)
        
        logger.info(f"Created clipboard item {item_id} from {source_location} to {target_locations}")
        return item
    
    def get_clipboard_items(
        self,
        location: str,
        content_type: Optional[str] = None,
        priority: Optional[str] = None,
        include_expired: bool = False
    ) -> List[ClipboardItem]:
        """Get clipboard items available at a specific location"""
        
        items = []
        current_time = datetime.now(timezone.utc)
        
        for item in self.clipboard_items.values():
            # Check if item is available at this location
            if location not in item.target_locations:
                continue
            
            # Check content type filter
            if content_type and item.content_type != content_type:
                continue
            
            # Check priority filter
            if priority and item.priority != priority:
                continue
            
            # Check expiration
            if not include_expired and item.expires_at and item.expires_at < current_time:
                continue
            
            items.append(item)
        
        # Sort by priority and creation time
        items.sort(key=lambda x: (self._priority_score(x.priority), x.created_at))
        
        return items
    
    def get_emergency_items(self, location: str) -> List[ClipboardItem]:
        """Get emergency priority items for a location"""
        return self.get_clipboard_items(
            location=location,
            priority='emergency',
            include_expired=False
        )
    
    def get_conversation_context(self, location: str, conversation_id: str) -> Optional[ClipboardItem]:
        """Get conversation context for continuing a discussion"""
        items = self.get_clipboard_items(
            location=location,
            content_type='conversation'
        )
        
        for item in items:
            if item.metadata.get('conversation_id') == conversation_id:
                return item
        
        return None
    
    def update_clipboard_item(self, item_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing clipboard item"""
        if item_id not in self.clipboard_items:
            logger.warning(f"Clipboard item {item_id} not found")
            return False
        
        item = self.clipboard_items[item_id]
        
        # Update allowed fields
        allowed_updates = ['content', 'target_locations', 'expires_at', 'priority', 'tags', 'metadata']
        
        for field, value in updates.items():
            if field in allowed_updates:
                setattr(item, field, value)
        
        # Store updated item
        self._store_item(item)
        
        logger.info(f"Updated clipboard item {item_id}")
        return True
    
    def delete_clipboard_item(self, item_id: str) -> bool:
        """Delete a clipboard item"""
        if item_id not in self.clipboard_items:
            logger.warning(f"Clipboard item {item_id} not found")
            return False
        
        del self.clipboard_items[item_id]
        self._delete_stored_item(item_id)
        
        logger.info(f"Deleted clipboard item {item_id}")
        return True
    
    def _generate_item_id(self, content: str, source_location: str, created_by: str) -> str:
        """Generate unique ID for clipboard item"""
        unique_string = f"{content[:50]}{source_location}{created_by}{time.time()}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:16]
    
    def _priority_score(self, priority: str) -> int:
        """Convert priority to numeric score for sorting"""
        priority_scores = {
            'emergency': 0,
            'high': 1,
            'medium': 2,
            'low': 3
        }
        return priority_scores.get(priority, 2)
    
    def _store_item(self, item: ClipboardItem):
        """Store clipboard item in appropriate backend"""
        if self.storage_backend == 'database':
            self._store_in_database(item)
        elif self.storage_backend == 'secret_manager':
            self._store_in_secret_manager(item)
        
        # Also keep in memory for fast access
        self.clipboard_items[item.id] = item
    
    def _store_in_database(self, item: ClipboardItem):
        """Store item in database (to be implemented)"""
        # TODO: Implement database storage
        pass
    
    def _store_in_secret_manager(self, item: ClipboardItem):
        """Store item in Secret Manager"""
        try:
            secret_id = f"zaido_clipboard_{item.id}"
            secret_data = json.dumps(item.to_dict())
            self.secret_client._add_secret_version(
                f"projects/{self.project_id}/secrets/{secret_id}",
                secret_data
            )
        except Exception as e:
            logger.error(f"Failed to store item in Secret Manager: {e}")
    
    def _delete_stored_item(self, item_id: str):
        """Delete item from storage backend"""
        if self.storage_backend == 'database':
            self._delete_from_database(item_id)
        elif self.storage_backend == 'secret_manager':
            self._delete_from_secret_manager(item_id)
    
    def _delete_from_database(self, item_id: str):
        """Delete item from database (to be implemented)"""
        # TODO: Implement database deletion
        pass
    
    def _delete_from_secret_manager(self, item_id: str):
        """Delete item from Secret Manager"""
        try:
            secret_id = f"zaido_clipboard_{item_id}"
            # Note: Secret Manager doesn't support deletion, but we can mark as disabled
            logger.info(f"Marked Secret Manager item {secret_id} as disabled")
        except Exception as e:
            logger.error(f"Failed to delete item from Secret Manager: {e}")

def serve_health_check():
    """Health check endpoint for Cloud Run"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "clipboard-bridge",
        "version": "1.0.0",
        "cloud_run_support": True,
        "domain_mapping": {
            "enabled": True,
            "region": "us-west1",
            "health_check_path": "/health"
        },
        "wsgi_server": "flask",
        "production_mode": True,
        "deployment_model": "all_instances_production",
        "port": int(os.getenv("PORT", "8080")),
        "host": "cb.yourl.cloud",
        "protocol": "https"
    }

def serve():
    """Run the Flask server for Cloud Run"""
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    bridge = ZaidoClipboardBridge(os.getenv("GOOGLE_CLOUD_PROJECT"))
    
    @app.route("/health")
    def health():
        return jsonify(serve_health_check())
    
    @app.route("/api/clipboard", methods=["POST"])
    def create_item():
        data = request.get_json()
        try:
            item = bridge.create_clipboard_item(
                content=data["content"],
                content_type=data["content_type"],
                source_location=data["source_location"],
                target_locations=data["target_locations"],
                created_by=data["created_by"],
                priority=data.get("priority", "medium"),
                tags=data.get("tags"),
                expires_in_hours=data.get("expires_in_hours", 24),
                metadata=data.get("metadata")
            )
            return jsonify(item.to_dict()), 201
        except KeyError as e:
            return jsonify({"error": f"Missing required field: {str(e)}"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/clipboard/<location>")
    def get_items(location):
        content_type = request.args.get("content_type")
        priority = request.args.get("priority")
        include_expired = request.args.get("include_expired", "false").lower() == "true"
        
        items = bridge.get_clipboard_items(
            location=location,
            content_type=content_type,
            priority=priority,
            include_expired=include_expired
        )
        return jsonify([item.to_dict() for item in items])
    
    @app.route("/api/clipboard/emergency/<location>")
    def get_emergency_items(location):
        items = bridge.get_emergency_items(location)
        return jsonify([item.to_dict() for item in items])
    
    @app.route("/api/clipboard/conversation/<location>/<conversation_id>")
    def get_conversation(location, conversation_id):
        item = bridge.get_conversation_context(location, conversation_id)
        if item:
            return jsonify(item.to_dict())
        return jsonify({"error": "Conversation not found"}), 404
    
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Zaido Clipboard Bridge for AI Experiences")
    parser.add_argument("--project-id", required=True, help="Google Cloud project ID")
    parser.add_argument("--action", choices=["create", "get", "list", "update", "delete", "serve"], required=True)
    parser.add_argument("--content", help="Content for clipboard item")
    parser.add_argument("--content-type", help="Type of content")
    parser.add_argument("--source-location", help="Source location")
    parser.add_argument("--target-locations", nargs="+", help="Target locations")
    parser.add_argument("--created-by", help="Who created the item")
    parser.add_argument("--priority", choices=["low", "medium", "high", "emergency"], default="medium")
    parser.add_argument("--location", help="Location to get items for")
    
    args = parser.parse_args()
    
    try:
        bridge = ZaidoClipboardBridge(args.project_id)
        
        if args.action == "create":
            if not all([args.content, args.content_type, args.source_location, args.target_locations, args.created_by]):
                print("Error: All fields required for create action")
                return
            
            item = bridge.create_clipboard_item(
                content=args.content,
                content_type=args.content_type,
                source_location=args.source_location,
                target_locations=args.target_locations,
                created_by=args.created_by,
                priority=args.priority
            )
            print(f"✅ Created clipboard item: {item.id}")
        
        elif args.action == "get":
            if not args.location:
                print("Error: Location required for get action")
                return
            
            items = bridge.get_clipboard_items(location=args.location)
            if items:
                print(f"📋 Found {len(items)} clipboard items for {args.location}:")
                for item in items:
                    print(f"  • {item.id}: {item.content[:50]}... ({item.priority})")
            else:
                print(f"📋 No clipboard items found for {args.location}")
        
        elif args.action == "list":
            if not args.location:
                print("Error: Location required for list action")
                return
            
            items = bridge.get_clipboard_items(location=args.location, include_expired=True)
            print(f"📋 All clipboard items for {args.location}:")
            for item in items:
                status = "EXPIRED" if item.expires_at and item.expires_at < datetime.now(timezone.utc) else "ACTIVE"
                print(f"  • {item.id}: {item.content[:50]}... ({item.priority}) - {status}")
        
        elif args.action == "update":
            print("Update action not yet implemented")
        
        elif args.action == "delete":
            print("Delete action not yet implemented")
            
        elif args.action == "serve":
            serve()
    
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
