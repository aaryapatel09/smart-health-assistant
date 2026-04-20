"""Smoke tests for the Flask API and model pipeline."""
from __future__ import annotations

import json

import pytest

import app as web_app
import model as mlmodel

HIGH_RISK = {
    "age": 63, "sex": 1, "cp": 4, "trestbps": 155, "chol": 275, "fbs": 1,
    "restecg": 2, "thalach": 115, "exang": 1, "oldpeak": 2.8, "slope": 3,
    "ca": 2, "thal": 7,
}
LOW_RISK = {
    "age": 30, "sex": 0, "cp": 3, "trestbps": 115, "chol": 175, "fbs": 0,
    "restecg": 0, "thalach": 180, "exang": 0, "oldpeak": 0.0, "slope": 1,
    "ca": 0, "thal": 3,
}


@pytest.fixture(scope="module")
def client():
    web_app.app.config["TESTING"] = True
    with web_app.app.test_client() as c:
        yield c


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_index_serves_spa(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"<!doctype html>" in r.data.lower()


def test_high_risk_scores_above_low_risk(client):
    rh = client.post("/api/predict", json=HIGH_RISK).get_json()
    rl = client.post("/api/predict", json=LOW_RISK).get_json()
    assert "probability" in rh and "probability" in rl
    assert rh["probability"] > rl["probability"]
    assert rh["risk_band"] in {"low", "moderate", "high"}
    assert rl["risk_band"] in {"low", "moderate", "high"}


def test_missing_fields_returns_400(client):
    r = client.post("/api/predict", json={"age": 35})
    assert r.status_code == 400
    assert "missing fields" in r.get_json()["error"]


def test_type_errors_are_rejected(client):
    bad = dict(LOW_RISK)
    bad["age"] = "thirty"
    r = client.post("/api/predict", json=bad)
    assert r.status_code == 400
    assert "numeric" in r.get_json()["error"]


def test_out_of_range_rejected(client):
    bad = dict(LOW_RISK)
    bad["age"] = 500
    r = client.post("/api/predict", json=bad)
    assert r.status_code == 400
    assert "out of range" in r.get_json()["error"]


def test_model_predict_row_matches_api(client):
    clf = web_app._clf
    api = client.post("/api/predict", json=HIGH_RISK).get_json()
    direct = mlmodel.predict(clf, HIGH_RISK)
    assert api["probability"] == pytest.approx(direct["probability"])
