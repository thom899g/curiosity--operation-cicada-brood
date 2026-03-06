"""
Firebase Firestore manager for state persistence and real-time coordination
"""
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, timedelta
import json
from cicada_config import FIREBASE_COLLECTIONS

logger = logging.getLogger(__name__)

class FirebaseManager:
    """Manages all Firebase Firestore operations for the daemon ecosystem"""
    
    def __init__(self, credential_path: Optional[str] = None):
        """Initialize Firebase connection"""
        try:
            if not firebase_admin._apps:
                if credential_path and os.path.exists(credential_path):
                    cred = credentials.Certificate(credential_path)
                else:
                    # Try environment variable or default credentials
                    cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            self._verify_collections()
            logger.info("Firebase Firestore initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            raise
    
    def _verify_collections(self) -> None:
        """Verify all required collections exist"""
        for collection_name in FIREBASE_COLLECTIONS.values():
            # Firestore creates collections implicitly on first document write
            # We'll just log the collection names
            logger.debug(f"Using collection: {collection_name}")
    
    def register_daemon(self, daemon_id: str, hypothesis: str, 
                       trading_pair: str, allocation: float) -> bool:
        """Register a new daemon in the system"""
        try:
            daemon_ref = self.db.collection(FIREBASE_COLLECTIONS['daemons']).document(daemon_id)
            
            daemon_data = {
                'daemon_id': daemon_id,
                'hypothesis': hypothesis,
                'trading_pair': trading_pair,
                'capital_allocation': allocation,
                'status': 'active',
                'created_at': SERVER_TIMESTAMP,
                'last_heartbeat': SERVER_TIMESTAMP,
                'pnl': 0.0,
                'trades_count': 0
            }
            
            daemon_ref.set(daemon_data)
            logger.info(f"Registered daemon {daemon_id} for {trading_pair}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register daemon {daemon_id}: {e}")
            return False
    
    def update_daemon_state(self, daemon_id: str, state_updates: Dict[str, Any]) -> bool:
        """Update daemon state with heartbeat"""
        try:
            daemon_ref = self.db.collection(FIREBASE_COLLECTIONS['daemons']).document(daemon_id)
            
            state_updates['last_heartbeat'] = SERVER_TIMESTAMP
            daemon_ref.update(state_updates)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update daemon {daemon_id}: {e}")
            return False
    
    def record_finding(self, daemon_id: str, finding_type: str, 
                      data: Dict[str, Any], confidence: float) -> bool:
        """Record a market anomaly finding"""
        try:
            findings_ref = self.db.collection(FIREBASE_COLLECTIONS['findings'])
            
            finding_data = {
                'daemon_id': daemon_id,
                'finding_type': finding_type,
                'data': json