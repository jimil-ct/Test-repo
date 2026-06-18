"""Cryptographic helpers for token encryption and hashing."""

import base64
import os

from cryptography.fernet import Fernet

ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY", Fernet.generate_key().decode())
_fernet = Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)


def encrypt_token(plaintext: str) -> str:
    """Encrypt a token string using Fernet symmetric encryption."""
    return _fernet.encrypt(plaintext.encode()).decode()


def decrypt_token(ciphertext: str) -> str:
    """Decrypt a Fernet-encrypted token."""
    return _fernet.decrypt(ciphertext.encode()).decode()


def generate_secure_random(length: int = 32) -> str:
    """Generate a cryptographically secure random hex string."""
    return os.urandom(length).hex()
