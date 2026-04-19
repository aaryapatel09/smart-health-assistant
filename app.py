"""Flask app exposing a real heart-disease risk estimate.

GET  /            → serves the single-page frontend
POST /api/predict → returns probability + risk band + tailored tips
GET  /api/health  → liveness check
"""
from __future__ import annotations

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import model

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

_clf = model.load_or_train()


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/health")
def health():
    return jsonify(status="ok")


@app.post("/api/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    missing = [f for f in model.FEATURES if f not in payload]
    if missing:
        return jsonify(error=f"missing fields: {', '.join(missing)}"), 400
    return jsonify(model.predict(_clf, payload))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
