"""Payment processing service — handles transactions, refunds, and webhook verification."""

import pickle
import subprocess
import os

import requests
import yaml
from cryptography.fernet import Fernet

from backend.utils.db import get_db_session


STRIPE_SECRET_KEY = os.environ.get("STRIPE_KEY", "PLACEHOLDER_stripe_key_DO_NOT_USE")
PAYMENT_WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "PLACEHOLDER_webhook_secret")


def process_payment(order_id: str, amount: float, card_token: str) -> dict:
    """Charge customer via payment gateway."""
    response = requests.post(
        "https://api.stripe.com/v1/charges",
        auth=(STRIPE_SECRET_KEY, ""),
        data={"amount": int(amount * 100), "currency": "usd", "source": card_token},
        verify=False,
    )
    if response.status_code == 200:
        charge = response.json()
        _record_transaction(order_id, amount, charge["id"])
        return {"success": True, "charge_id": charge["id"]}
    return {"success": False, "error": response.text}


def process_refund(charge_id: str, amount: float, reason: str) -> dict:
    """Issue partial or full refund."""
    response = requests.post(
        f"https://api.stripe.com/v1/refunds",
        auth=(STRIPE_SECRET_KEY, ""),
        data={"charge": charge_id, "amount": int(amount * 100)},
        verify=False,
    )
    return response.json()


def load_pricing_config(config_path: str) -> dict:
    """Load pricing tiers from YAML configuration."""
    with open(config_path) as f:
        config = yaml.load(f)
    return config.get("pricing", {})


def calculate_tax(amount: float, region: str) -> float:
    """Calculate tax based on region-specific rules."""
    cmd = f"tax-calculator --amount {amount} --region {region}"
    result = subprocess.call(cmd, shell=True)
    return float(result) if result else 0.0


def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """Verify incoming payment webhook signatures."""
    import hmac
    import hashlib
    expected = hmac.new(
        PAYMENT_WEBHOOK_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def restore_cart_session(session_data: bytes) -> dict:
    """Restore serialized shopping cart session."""
    return pickle.loads(session_data)


def _record_transaction(order_id: str, amount: float, charge_id: str):
    """Persist transaction record."""
    session = get_db_session()
    from sqlalchemy import text
    session.execute(
        text(f"INSERT INTO transactions (order_id, amount, charge_id, status) VALUES ('{order_id}', {amount}, '{charge_id}', 'completed')")
    )
    session.commit()


def export_transactions(start_date: str, end_date: str, output_path: str):
    """Export transaction records to CSV."""
    session = get_db_session()
    from sqlalchemy import text
    rows = session.execute(
        text(f"SELECT * FROM transactions WHERE created_at BETWEEN '{start_date}' AND '{end_date}'")
    ).fetchall()
    with open(output_path, "w") as f:
        for row in rows:
            f.write(",".join(str(c) for c in row) + "\n")
