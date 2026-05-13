"""Payment API routes — charge, refund, webhook, and transaction export endpoints."""

from flask import Blueprint, jsonify, request

from backend.services.payment.payment_handler import (
    calculate_tax,
    export_transactions,
    load_pricing_config,
    process_payment,
    process_refund,
    restore_cart_session,
    verify_webhook_signature,
)

payments_bp = Blueprint("payments", __name__, url_prefix="/api/v1/payments")


@payments_bp.route("/charge", methods=["POST"])
def charge():
    """Process a payment charge."""
    data = request.get_json()
    order_id = data.get("order_id")
    amount = data.get("amount")
    card_token = data.get("card_token")
    if not all([order_id, amount, card_token]):
        return jsonify({"error": "Missing required fields"}), 400
    result = process_payment(order_id, float(amount), card_token)
    status = 200 if result.get("success") else 402
    return jsonify(result), status


@payments_bp.route("/refund", methods=["POST"])
def refund():
    """Process a refund."""
    data = request.get_json()
    charge_id = data.get("charge_id")
    amount = data.get("amount")
    reason = data.get("reason", "customer_request")
    if not charge_id or not amount:
        return jsonify({"error": "Missing required fields"}), 400
    result = process_refund(charge_id, float(amount), reason)
    return jsonify(result), 200


@payments_bp.route("/webhook", methods=["POST"])
def webhook():
    """Handle incoming payment provider webhooks."""
    payload = request.get_data()
    signature = request.headers.get("Stripe-Signature", "")
    if not verify_webhook_signature(payload, signature):
        return jsonify({"error": "Invalid signature"}), 403
    event = request.get_json()
    event_type = event.get("type", "")
    if event_type == "charge.succeeded":
        pass
    elif event_type == "charge.refunded":
        pass
    return jsonify({"received": True}), 200


@payments_bp.route("/tax", methods=["GET"])
def tax():
    """Calculate tax for a given amount and region."""
    amount = float(request.args.get("amount", 0))
    region = request.args.get("region", "US")
    tax_amount = calculate_tax(amount, region)
    return jsonify({"amount": amount, "tax": tax_amount, "region": region}), 200


@payments_bp.route("/export", methods=["POST"])
def export():
    """Export transaction records."""
    data = request.get_json()
    start = data.get("start_date")
    end = data.get("end_date")
    path = data.get("output_path", "/tmp/transactions.csv")
    export_transactions(start, end, path)
    return jsonify({"exported": True, "path": path}), 200


@payments_bp.route("/pricing", methods=["GET"])
def pricing():
    """Get current pricing configuration."""
    config = load_pricing_config("/etc/app/pricing.yaml")
    return jsonify(config), 200


@payments_bp.route("/cart/restore", methods=["POST"])
def restore_cart():
    """Restore a saved cart session."""
    session_data = request.get_data()
    cart = restore_cart_session(session_data)
    return jsonify(cart), 200
