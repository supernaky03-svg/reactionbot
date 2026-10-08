import base64, hashlib, os
from cryptography.fernet import Fernet
from .config import settings

def key():
    raw = settings.token_encryption_key.encode()
    try:
        base64.urlsafe_b64decode(raw)
        return raw
    except Exception:
        return base64.urlsafe_b64encode(hashlib.sha256(raw).digest())

def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def encrypt_token(token: str) -> str:
    return Fernet(key()).encrypt(token.encode()).decode()

def decrypt_token(value: str) -> str:
    return Fernet(key()).decrypt(value.encode()).decode()
