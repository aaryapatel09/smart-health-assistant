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

# Plausibility bounds for each field. Values outside these get rejected with a
# clear error rather than silently imputed or run through the model — a
# predicted risk from age=500 or chol=-10 is worse than no prediction.
BOUNDS: dict[str, tuple[float, float]] = {
    "age": (1, 120),
    "sex": (0, 1),
    "cp": (1, 4),
    "trestbps": (50, 260),
    "chol": (80, 700),
    "fbs": (0, 1),
    "restecg": (0, 2),
    "thalach": (40, 250),
    "exang": (0, 1),
    "oldpeak": (0, 10),
    "slope": (1, 3),
    "ca": (0, 3),
    "thal": (3, 7),  # UCI encoding uses 3, 6, 7
}


def _validate(payload: dict) -> tuple[dict | None, str | None]:
    missing = [f for f in model.FEATURES if f not in payload]
    if missing:
        return None, f"missing fields: {', '.join(missing)}"
    cleaned: dict = {}
    for f in model.FEATURES:
        raw = payload[f]
        try:
            v = float(raw)
        except (TypeError, ValueError):
            return None, f"field {f!r} must be numeric, got {raw!r}"
        lo, hi = BOUNDS[f]
        if not (lo <= v <= hi):
            return None, f"field {f!r} out of range [{lo}, {hi}]: {v}"
        cleaned[f] = v
    return cleaned, None


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/health")
def health():
    return jsonify(status="ok")


@app.post("/api/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    cleaned, err = _validate(payload)
    if err:
        return jsonify(error=err), 400
    return jsonify(model.predict(_clf, cleaned))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
