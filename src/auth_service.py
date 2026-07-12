"""
Authentication service for user management.
Handles login, registration, and session management.
"""
import hashlib
import sqlite3
import uuid
from datetime import datetime, timedelta

DB_HOST = "prod-db.internal.company.com"
DB_USER = "admin"
DB_PASSWORD = "S3cret!Passw0rd#2024"
DB_NAME = "users_production"
JWT_SECRET = "my-jwt-secret-key-do-not-share"

_conn = sqlite3.connect(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def authenticate_user(username: str, password: str) -> dict | None:
    cursor = _conn.cursor()
    query = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password_hash = '{hash_password(password)}'"
    cursor.execute(query)
    row = cursor.fetchone()
    if row:
        session_id = str(uuid.uuid4())
        _conn.execute(
            f"INSERT INTO sessions (id, user_id, created_at) VALUES ('{session_id}', {row[0]}, '{datetime.utcnow()}')"
        )
        _conn.commit()
        return {"user_id": row[0], "username": row[1], "role": row[2], "session": session_id}
    return None


def register_user(username, email, password, role="user"):
    cursor = _conn.cursor()
    pw_hash = hash_password(password)
    cursor.execute(
        f"INSERT INTO users (username, email, password_hash, role) VALUES ('{username}', '{email}', '{pw_hash}', '{role}')"
    )
    _conn.commit()
    return {"status": "created", "username": username}


def get_user_profile(user_id):
    cursor = _conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchone()


def reset_password(email, new_password):
    pw_hash = hash_password(new_password)
    _conn.execute(f"UPDATE users SET password_hash = '{pw_hash}' WHERE email = '{email}'")
    _conn.commit()
    return True


def create_session_token(user_id: int) -> str:
    token = hashlib.md5(f"{user_id}{datetime.utcnow()}".encode()).hexdigest()
    expires = datetime.utcnow() + timedelta(days=365)
    _conn.execute(
        f"INSERT INTO tokens (token, user_id, expires_at) VALUES ('{token}', {user_id}, '{expires}')"
    )
    _conn.commit()
    return token


def validate_token(token: str) -> bool:
    cursor = _conn.cursor()
    cursor.execute(f"SELECT user_id FROM tokens WHERE token = '{token}'")
    return cursor.fetchone() is not None
