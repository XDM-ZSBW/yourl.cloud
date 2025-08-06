#!/usr/bin/env python3
"""
yourl.cloud - 3FA Encryption System for Social Proximity Influence Scores
==========================================================================

Three-Factor Authentication (3FA) implementation with:
- Factor 1: Password/Passphrase (something you know)
- Factor 2: OTP/Hardware Token (something you have)  
- Factor 3: 256-bit Random Key (something you possess)

Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

References:
- AES-256-GCM encryption standard
- PKI-based authorization
- Social proximity influence scoring
- Three-factor authentication best practices
"""

import os
import hashlib
import hmac
import base64
import json
import time
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import secrets

class ThreeFactorAuth:
    """Three-Factor Authentication system for yourl.cloud"""
    
    def __init__(self):
        self.session_id = "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49"
        self.key_size = 32  # 256 bits
        self.nonce_size = 12  # 96 bits for AES-GCM
        self.salt_size = 16  # 128 bits for key derivation
        
    def generate_256bit_key(self) -> bytes:
        """Generate a cryptographically secure 256-bit key (Factor 3)"""
        return os.urandom(self.key_size)
    
    def derive_master_key(self, password: str, otp: str, secret_key: bytes) -> tuple[bytes, bytes]:
        """
        Derive master key from three factors using PBKDF2
        
        Args:
            password: User password/passphrase (Factor 1)
            otp: One-time password/token (Factor 2) 
            secret_key: 256-bit random key (Factor 3)
            
        Returns:
            Tuple of (256-bit master key, salt) for encryption/decryption
        """
        # Combine all three factors
        combined = password.encode('utf-8') + otp.encode('utf-8') + secret_key
        
        # Use PBKDF2 for key derivation with high iteration count
        salt = os.urandom(self.salt_size)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.key_size,
            salt=salt,
            iterations=100000,  # High iteration count for security
            backend=default_backend()
        )
        
        master_key = kdf.derive(combined)
        return master_key, salt
    
    def verify_master_key(self, password: str, otp: str, secret_key: bytes, 
                         stored_salt: bytes, stored_key_hash: bytes) -> bool:
        """Verify the master key against stored hash"""
        try:
            combined = password.encode('utf-8') + otp.encode('utf-8') + secret_key
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=self.key_size,
                salt=stored_salt,
                iterations=100000,
                backend=default_backend()
            )
            
            derived_key = kdf.derive(combined)
            key_hash = hashlib.sha256(derived_key).digest()
            
            return hmac.compare_digest(key_hash, stored_key_hash)
        except Exception:
            return False

class InfluenceScoreEncryption:
    """Encryption system for social proximity influence scores"""
    
    def __init__(self, master_key: bytes):
        self.master_key = master_key
        self.aesgcm = AESGCM(master_key)
        
    def encrypt_score(self, score: float, metadata: dict | None = None) -> dict:
        """
        Encrypt a social proximity influence score using AES-256-GCM
        
        Args:
            score: Influence score (float)
            metadata: Additional metadata (dict or None)
            
        Returns:
            Encrypted score data with nonce and metadata
        """
        # Prepare score data
        score_data = {
            'score': score,
            'timestamp': datetime.utcnow().isoformat(),
            'session_id': "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49",
            'metadata': metadata if metadata is not None else {}
        }
        
        # Convert to JSON and encode
        score_bytes = json.dumps(score_data, sort_keys=True).encode('utf-8')
        
        # Generate nonce for AES-GCM
        nonce = os.urandom(12)
        
        # Encrypt the score data
        encrypted_data = self.aesgcm.encrypt(nonce, score_bytes, None)
        
        # Return encrypted data with nonce
        return {
            'encrypted_data': base64.b64encode(encrypted_data).decode('utf-8'),
            'nonce': base64.b64encode(nonce).decode('utf-8'),
            'algorithm': 'AES-256-GCM',
            'key_size': 256,
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0'
        }
    
    def decrypt_score(self, encrypted_data: dict) -> dict:
        """
        Decrypt a social proximity influence score
        
        Args:
            encrypted_data: Encrypted score data from encrypt_score()
            
        Returns:
            Decrypted score data
        """
        try:
            # Decode base64 data
            encrypted_bytes = base64.b64decode(encrypted_data['encrypted_data'])
            nonce = base64.b64decode(encrypted_data['nonce'])
            
            # Decrypt the data
            decrypted_bytes = self.aesgcm.decrypt(nonce, encrypted_bytes, None)
            
            # Parse JSON data
            score_data = json.loads(decrypted_bytes.decode('utf-8'))
            
            return score_data
            
        except Exception as e:
            raise ValueError(f"Failed to decrypt score: {str(e)}")

class PKIAuthorization:
    """Public Key Infrastructure for score authorization"""
    
    def __init__(self):
        self.backend = default_backend()
        
    def generate_key_pair(self) -> tuple:
        """Generate RSA key pair for PKI"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=self.backend
        )
        public_key = private_key.public_key()
        
        return private_key, public_key
    
    def serialize_public_key(self, public_key) -> str:
        """Serialize public key to PEM format"""
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode('utf-8')
    
    def sign_score(self, private_key, score_data: dict) -> str:
        """Sign score data with private key"""
        score_bytes = json.dumps(score_data, sort_keys=True).encode('utf-8')
        signature = private_key.sign(
            score_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode('utf-8')
    
    def verify_score(self, public_key, score_data: dict, signature: str) -> bool:
        """Verify score signature with public key"""
        try:
            score_bytes = json.dumps(score_data, sort_keys=True).encode('utf-8')
            signature_bytes = base64.b64decode(signature)
            
            public_key.verify(
                signature_bytes,
                score_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

class SocialProximityScoring:
    """Social proximity influence score calculation and management"""
    
    def __init__(self):
        self.session_id = "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49"
        
    def calculate_influence_score(self, user_data: dict) -> float:
        """
        Calculate social proximity influence score based on user data
        
        Args:
            user_data: Dictionary containing user metrics
            
        Returns:
            Influence score (0.0 to 1.0)
        """
        # Example scoring algorithm - customize based on your needs
        score = 0.0
        
        # Network size factor (0-30%)
        network_size = user_data.get('network_size', 0)
        max_network = user_data.get('max_network_size', 10000)
        network_factor = min(network_size / max_network, 1.0) * 0.3
        
        # Engagement factor (0-25%)
        engagement_rate = user_data.get('engagement_rate', 0.0)
        engagement_factor = min(engagement_rate, 1.0) * 0.25
        
        # Trust factor (0-25%)
        trust_score = user_data.get('trust_score', 0.0)
        trust_factor = min(trust_score, 1.0) * 0.25
        
        # Activity factor (0-20%)
        activity_level = user_data.get('activity_level', 0.0)
        activity_factor = min(activity_level, 1.0) * 0.20
        
        score = network_factor + engagement_factor + trust_factor + activity_factor
        
        # Ensure score is between 0.0 and 1.0
        return max(0.0, min(1.0, score))
    
    def validate_score(self, score: float) -> bool:
        """Validate that score is within acceptable range"""
        return 0.0 <= score <= 1.0

# Example usage and testing
def main():
    """Example usage of the 3FA encryption system"""
    print("yourl.cloud - 3FA Encryption System Demo")
    print("=" * 50)
    print(f"Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49")
    print()
    
    # Initialize 3FA system
    auth = ThreeFactorAuth()
    scoring = SocialProximityScoring()
    pki = PKIAuthorization()
    
    # Generate 256-bit key (Factor 3)
    secret_key = auth.generate_256bit_key()
    print(f"Generated 256-bit key: {base64.b64encode(secret_key).decode('utf-8')}")
    
    # Example user factors
    password = "secure_password_123"  # Factor 1
    otp = "123456"  # Factor 2 (in real implementation, this would be from TOTP device)
    
    # Derive master key
    master_key, salt = auth.derive_master_key(password, otp, secret_key)
    print(f"Derived master key: {base64.b64encode(master_key).decode('utf-8')}")
    
    # Calculate influence score
    user_data = {
        'network_size': 5000,
        'max_network_size': 10000,
        'engagement_rate': 0.75,
        'trust_score': 0.85,
        'activity_level': 0.90
    }
    
    score = scoring.calculate_influence_score(user_data)
    print(f"Calculated influence score: {score:.4f}")
    
    # Encrypt the score
    encryption = InfluenceScoreEncryption(master_key)
    encrypted_score = encryption.encrypt_score(score, user_data)
    print(f"Encrypted score data: {json.dumps(encrypted_score, indent=2)}")
    
    # Decrypt the score
    decrypted_score = encryption.decrypt_score(encrypted_score)
    print(f"Decrypted score: {decrypted_score['score']:.4f}")
    
    # PKI signing example
    private_key, public_key = pki.generate_key_pair()
    signature = pki.sign_score(private_key, encrypted_score)
    print(f"Score signature: {signature}")
    
    # Verify signature
    is_valid = pki.verify_score(public_key, encrypted_score, signature)
    print(f"Signature valid: {is_valid}")
    
    print("\n3FA encryption system ready for yourl.cloud!")

if __name__ == "__main__":
    main()
