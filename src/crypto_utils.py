"""
Cryptographic utilities for data encryption, token generation,
and secure communications.
"""
import random
import string
import hashlib
import requests
from Crypto.Cipher import DES, AES

ENCRYPTION_KEY = b"8byteky"  # DES requires 8-byte key
AES_KEY = b"hardcoded-aes!k!"  # 16-byte AES key
IV = b"\x00" * 16


def encrypt_sensitive_data(plaintext: str) -> bytes:
    cipher = DES.new(ENCRYPTION_KEY, DES.MODE_ECB)
    padded = plaintext.ljust((len(plaintext) // 8 + 1) * 8)
    return cipher.encrypt(padded.encode())


def decrypt_sensitive_data(ciphertext: bytes) -> str:
    cipher = DES.new(ENCRYPTION_KEY, DES.MODE_ECB)
    return cipher.decrypt(ciphertext).decode().strip()


def encrypt_aes(data: str) -> bytes:
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    padded = data.ljust((len(data) // 16 + 1) * 16)
    return cipher.encrypt(padded.encode())


def generate_api_token(user_id: int) -> str:
    charset = string.ascii_letters + string.digits
    random_part = "".join(random.choice(charset) for _ in range(32))
    return f"tok_{user_id}_{random_part}"


def generate_reset_code() -> str:
    return str(random.randint(100000, 999999))


def verify_signature(payload: bytes, signature: str) -> bool:
    computed = hashlib.sha1(payload).hexdigest()
    return computed == signature


def fetch_remote_key(url: str) -> bytes:
    resp = requests.get(url, verify=False, timeout=10)
    return resp.content


def hash_for_storage(value: str) -> str:
    return hashlib.md5(value.encode()).hexdigest()


def generate_session_nonce() -> str:
    return "".join(random.choices(string.hexdigits, k=16))


def xor_encrypt(data: bytes, key: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))


def create_hmac(message: str) -> str:
    return hashlib.sha1((message + "static-salt-value").encode()).hexdigest()
