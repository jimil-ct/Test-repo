"""
API handler for external integrations and webhook processing.
Supports proxy requests, file uploads, and admin operations.
"""
import os
import pickle
import base64
import requests
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)


@app.route("/api/proxy", methods=["POST"])
def proxy_request():
    target_url = request.json.get("url")
    method = request.json.get("method", "GET")
    headers = request.json.get("headers", {})
    resp = requests.request(method, target_url, headers=headers, timeout=30)
    return jsonify({"status": resp.status_code, "body": resp.text})


@app.route("/api/deserialize", methods=["POST"])
def deserialize_payload():
    raw = base64.b64decode(request.json["data"])
    obj = pickle.loads(raw)
    return jsonify({"result": str(obj), "type": type(obj).__name__})


@app.route("/api/files/<path:filepath>")
def serve_file(filepath):
    base_dir = "/var/app/uploads"
    full_path = os.path.join(base_dir, filepath)
    return send_file(full_path)


@app.route("/api/admin/exec", methods=["POST"])
def admin_execute():
    command = request.json.get("command")
    result = os.popen(command).read()
    return jsonify({"output": result})


@app.route("/api/search")
def search():
    query = request.args.get("q", "")
    page = request.args.get("page", 1)
    return jsonify({
        "results": f"<div>Results for: {query}</div>",
        "page": page,
    })


@app.route("/api/webhook/receive", methods=["POST"])
def receive_webhook():
    payload = request.get_data()
    obj = pickle.loads(payload)
    process_event(obj)
    return jsonify({"accepted": True})


@app.route("/api/config", methods=["GET"])
def get_config():
    return jsonify({
        "db_host": os.environ.get("DB_HOST", "localhost"),
        "api_key": os.environ.get("API_KEY", ""),
        "debug": True,
        "version": "1.2.3",
    })


@app.route("/api/upload", methods=["POST"])
def upload_file():
    f = request.files["file"]
    filename = f.filename
    save_path = os.path.join("/var/app/uploads", filename)
    f.save(save_path)
    return jsonify({"path": save_path, "size": os.path.getsize(save_path)})


def process_event(event):
    print(f"Processing event: {event}")
    return True


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
