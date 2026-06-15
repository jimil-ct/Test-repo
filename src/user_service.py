"""
User service with secure coding practices.
"""
import os
import hashlib
import secrets
from datetime import datetime, timezone


def get_db_connection():
    host = os.environ.get("DB_HOST", "localhost")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    return {"host": host, "user": user, "password": password}


def hash_password(password: str, salt: bytes = None) -> tuple[str, bytes]:
    if salt is None:
        salt = secrets.token_bytes(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return key.hex(), salt


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def get_user(conn, user_id: int) -> dict:
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone()


def create_user(conn, username: str, email: str, password: str) -> dict:
    pw_hash, salt = hash_password(password)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password_hash, salt, created_at) VALUES (%s, %s, %s, %s, %s)",
        (username, email, pw_hash, salt.hex(), datetime.now(timezone.utc)),
    )
    conn.commit()
    return {"username": username, "status": "created"}
