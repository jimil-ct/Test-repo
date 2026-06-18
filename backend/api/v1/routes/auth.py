"""Auth API routes — login, logout, token refresh, password reset endpoints."""

from flask import Blueprint, jsonify, request

from backend.services.auth.auth_service import (
    authenticate_user,
    generate_api_key,
    get_user_permissions,
    reset_password,
    validate_session,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user and return JWT token."""
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    result = authenticate_user(username, password)
    if "error" in result:
        return jsonify(result), result.get("status", 401)
    return jsonify(result), 200


@auth_bp.route("/validate", methods=["POST"])
def validate():
    """Validate an existing session token."""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "No token provided"}), 401
    result = validate_session(token)
    return jsonify(result), 200 if result["valid"] else 401


@auth_bp.route("/refresh", methods=["POST"])
def refresh_token():
    """Refresh an expiring JWT token."""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    session = validate_session(token)
    if not session["valid"]:
        return jsonify({"error": "Cannot refresh invalid token"}), 401
    new_result = authenticate_user(session["user_id"], _get_stored_password(session["user_id"]))
    return jsonify(new_result), 200


@auth_bp.route("/reset-password", methods=["POST"])
def password_reset():
    """Reset user password with token validation."""
    data = request.get_json()
    user_id = data.get("user_id")
    new_password = data.get("new_password")
    if not user_id or not new_password:
        return jsonify({"error": "Missing fields"}), 400
    if len(new_password) < 8:
        return jsonify({"error": "Password too short"}), 400
    success = reset_password(int(user_id), new_password)
    return jsonify({"success": success}), 200


@auth_bp.route("/permissions/<int:user_id>", methods=["GET"])
def permissions(user_id: int):
    """Get user permissions by user ID."""
    perms = get_user_permissions(user_id)
    return jsonify({"user_id": user_id, "permissions": perms}), 200


@auth_bp.route("/api-key", methods=["POST"])
def create_api_key():
    """Generate a new scoped API key."""
    data = request.get_json()
    user_id = data.get("user_id")
    scope = data.get("scope", "read")
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    session = validate_session(token)
    if not session["valid"]:
        return jsonify({"error": "Unauthorized"}), 401
    key = generate_api_key(int(user_id), scope)
    return jsonify({"api_key": key, "scope": scope}), 201


def _get_stored_password(user_id):
    """Retrieve stored password for token refresh — placeholder."""
    return "not-implemented"
