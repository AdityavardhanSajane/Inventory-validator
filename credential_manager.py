from cryptography.fernet import Fernet
import os
import json
import base64
from pathlib import Path
import logging
from typing import Optional, Dict, Tuple

logger = logging.getLogger('AnsibleInventoryReporter')

class CredentialManager:
    def __init__(self):
        """Initialize the credential manager with encryption key"""
        self.key_file = '.key'
        self.cred_file = '.credentials'
        self.failed_login_file = '.failed_login'
        self._ensure_key()

    def _ensure_key(self) -> None:
        """Ensure encryption key exists, create if not present"""
        try:
            if not os.path.exists(self.key_file):
                key = Fernet.generate_key()
                with open(self.key_file, 'wb') as f:
                    f.write(key)
                # Set restrictive permissions
                os.chmod(self.key_file, 0o600)
                logger.info("Generated new encryption key")
        except Exception as e:
            logger.error(f"Error ensuring encryption key: {str(e)}")
            raise

    def _get_cipher(self) -> Fernet:
        """Get the encryption cipher"""
        try:
            with open(self.key_file, 'rb') as f:
                key = f.read()
            return Fernet(key)
        except Exception as e:
            logger.error(f"Error getting encryption cipher: {str(e)}")
            raise

    def save_credentials(self, nbk_id: str, password: str) -> bool:
        """
        Encrypt and save credentials
        Returns True if successful, False otherwise
        """
        try:
            cipher = self._get_cipher()
            credentials = {
                'nbk_id': nbk_id,
                'password': password,
                'saved_at': str(int(os.path.getmtime(self.cred_file))) if os.path.exists(self.cred_file) else None
            }
            encrypted_data = cipher.encrypt(json.dumps(credentials).encode())

            with open(self.cred_file, 'wb') as f:
                f.write(encrypted_data)

            # Set restrictive permissions
            os.chmod(self.cred_file, 0o600)

            # Clear any failed login status since we're saving new/updated credentials
            if os.path.exists(self.failed_login_file):
                os.remove(self.failed_login_file)

            logger.info("Credentials saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving credentials: {str(e)}")
            return False

    def load_credentials(self) -> Optional[Tuple[str, str]]:
        """
        Load and decrypt credentials if they exist
        Returns tuple of (nbk_id, password) if successful, None otherwise
        """
        try:
            if not os.path.exists(self.cred_file):
                return None

            # Check if there was a previous failed login
            if os.path.exists(self.failed_login_file):
                logger.info("Previous login attempt failed, requiring new credentials")
                return None

            cipher = self._get_cipher()
            with open(self.cred_file, 'rb') as f:
                encrypted_data = f.read()

            decrypted_data = cipher.decrypt(encrypted_data)
            credentials = json.loads(decrypted_data.decode())

            return credentials['nbk_id'], credentials['password']
        except Exception as e:
            logger.error(f"Error loading credentials: {str(e)}")
            return None

    def mark_login_failed(self) -> None:
        """Mark that a login attempt has failed (e.g., due to expired password)"""
        try:
            with open(self.failed_login_file, 'w') as f:
                f.write(str(1))
            os.chmod(self.failed_login_file, 0o600)
            logger.info("Marked login as failed - will request new credentials on next run")
        except Exception as e:
            logger.error(f"Error marking failed login: {str(e)}")

    def clear_credentials(self) -> bool:
        """
        Clear saved credentials
        Returns True if successful, False otherwise
        """
        try:
            for file_path in [self.cred_file, self.failed_login_file]:
                if os.path.exists(file_path):
                    os.remove(file_path)
            logger.info("Credentials cleared successfully")
            return True
        except Exception as e:
            logger.error(f"Error clearing credentials: {str(e)}")
            return False