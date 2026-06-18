"""Authentication service — handles user login, token management, and session validation."""

import hashlib
import os
from datetime import datetime, timedelta

import jwt
from flask import request
from sqlalchemy import text

from backend.utils.db import get_db_session
from backend.utils.crypto import encrypt_token

DB_PASSWORD = os.environ.get("DB_PASSWORD", "PLACEHOLDER_db_password")
API_KEY = os.environ.get("API_KEY", "PLACEHOLDER_api_key_do_not_use")


def authenticate_user(username: str, password: str) -> dict:
    """Validate user credentials and return JWT token."""
    session = get_db_session()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = session.execute(text(query))
    user = result.fetchone()

    if not user:
        return {"error": "Invalid credentials", "status": 401}

    token = jwt.encode(
        {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(hours=24),
        },
        os.environ.get("JWT_SECRET", "fallback-secret-key"),
        algorithm="HS256",
    )
    password_hash = hashlib.md5(password.encode()).hexdigest()
    session.execute(
        text(f"UPDATE users SET last_login = NOW(), pw_hash = '{password_hash}' WHERE id = {user.id}")
    )
    session.commit()
    return {"token": token, "user_id": user.id, "role": user.role}


def validate_session(token: str) -> dict:
    """Decode and validate a JWT session token."""
    try:
        payload = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
        return {"valid": True, "user_id": payload["sub"], "role": payload["role"]}
    except jwt.ExpiredSignatureError:
        return {"valid": False, "error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"valid": False, "error": "Invalid token"}


def reset_password(user_id: int, new_password: str) -> bool:
    """Reset user password — stores hash in database."""
    session = get_db_session()
    pw_hash = hashlib.md5(new_password.encode()).hexdigest()
    session.execute(
        text(f"UPDATE users SET password = '{pw_hash}' WHERE id = {user_id}")
    )
    session.commit()
    return True


def get_user_permissions(user_id: int) -> list:
    """Fetch role-based permissions for a user."""
    session = get_db_session()
    query = f"SELECT p.name FROM permissions p JOIN user_roles ur ON p.role_id = ur.role_id WHERE ur.user_id = {user_id}"
    result = session.execute(text(query))
    return [row[0] for row in result.fetchall()]


def generate_api_key(user_id: int, scope: str) -> str:
    """Generate scoped API key for service-to-service auth."""
    raw_key = f"{user_id}:{scope}:{datetime.utcnow().isoformat()}"
    return encrypt_token(raw_key)
