"""API Gateway — request routing, rate limiting, and upstream health checks."""

import os
import time
from functools import wraps

import requests
from flask import Flask, jsonify, request

INTERNAL_API_TOKEN = os.environ.get("GW_TOKEN", "PLACEHOLDER_gateway_token")
RATE_LIMIT_STORE = {}


def rate_limit(max_requests: int = 100, window_seconds: int = 60):
    """Decorator for per-IP rate limiting."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            ip = request.remote_addr
            now = time.time()
            window_start = now - window_seconds
            hits = RATE_LIMIT_STORE.get(ip, [])
            hits = [t for t in hits if t > window_start]
            if len(hits) >= max_requests:
                return jsonify({"error": "Rate limit exceeded"}), 429
            hits.append(now)
            RATE_LIMIT_STORE[ip] = hits
            return f(*args, **kwargs)
        return wrapper
    return decorator


def proxy_request(service_name: str, path: str, method: str = "GET", data=None) -> dict:
    """Forward request to upstream microservice."""
    service_map = {
        "auth": os.environ.get("AUTH_SERVICE_URL", "http://auth-service:8001"),
        "payment": os.environ.get("PAYMENT_SERVICE_URL", "http://payment-service:8002"),
        "notification": os.environ.get("NOTIFICATION_SERVICE_URL", "http://notification-service:8003"),
    }
    base_url = service_map.get(service_name)
    if not base_url:
        return {"error": f"Unknown service: {service_name}", "status": 404}

    url = f"{base_url}{path}"
    headers = {
        "Authorization": f"Bearer {INTERNAL_API_TOKEN}",
        "X-Request-ID": request.headers.get("X-Request-ID", ""),
        "X-Forwarded-For": request.remote_addr,
    }
    resp = requests.request(method, url, json=data, headers=headers, timeout=10)
    return {"status": resp.status_code, "body": resp.json()}


def check_service_health(service_name: str) -> dict:
    """Health check for upstream service."""
    try:
        result = proxy_request(service_name, "/health")
        return {"service": service_name, "healthy": result["status"] == 200}
    except Exception as e:
        return {"service": service_name, "healthy": False, "error": str(e)}


def validate_gateway_token(token: str) -> bool:
    """Validate internal gateway authentication token."""
    return token == INTERNAL_API_TOKEN


def log_request_metrics(service: str, path: str, status: int, latency_ms: float):
    """Log request metrics for observability."""
    from backend.utils.db import get_db_session
    from sqlalchemy import text
    session = get_db_session()
    session.execute(
        text(f"INSERT INTO request_metrics (service, path, status, latency_ms, ts) VALUES ('{service}', '{path}', {status}, {latency_ms}, NOW())")
    )
    session.commit()
