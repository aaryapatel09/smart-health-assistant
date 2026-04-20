"""Heart disease classifier trained on the UCI Cleveland dataset.

https://archive.ics.uci.edu/ml/datasets/Heart+Disease

Target is binarized: any diagnosis of heart disease (num > 0) → 1.
"""
from __future__ import annotations

import os

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

COLUMNS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num",
]
FEATURES = COLUMNS[:-1]
NUMERIC_FEATURES = ["age", "trestbps", "chol", "thalach", "oldpeak"]
CATEGORICAL_FEATURES = ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"]

FEATURE_LABELS = {
    "age": "Age",
    "sex": "Sex",
    "cp": "Chest-pain type",
    "trestbps": "Resting blood pressure",
    "chol": "Cholesterol",
    "fbs": "Fasting blood sugar > 120",
    "restecg": "Resting ECG",
    "thalach": "Max heart rate",
    "exang": "Exercise-induced angina",
    "oldpeak": "ST depression (oldpeak)",
    "slope": "ST slope",
    "ca": "Major vessels colored",
    "thal": "Thallium stress test",
}

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "data", "cleveland.data")
MODEL_PATH = os.path.join(HERE, "data", "heart_model.joblib")
BASELINE_PATH = os.path.join(HERE, "data", "heart_baseline.joblib")


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, header=None, names=COLUMNS, na_values="?")
    df["target"] = (df["num"] > 0).astype(int)
    return df


def build_pipeline() -> Pipeline:
    preproc = ColumnTransformer([
        ("num", Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]), NUMERIC_FEATURES),
        ("cat", Pipeline([
            ("impute", SimpleImputer(strategy="most_frequent")),
        ]), CATEGORICAL_FEATURES),
    ])
    return Pipeline([
        ("pre", preproc),
        ("clf", GradientBoostingClassifier(n_estimators=200, max_depth=3, random_state=42)),
    ])


def _compute_baseline(df: pd.DataFrame) -> dict:
    """Typical-patient profile used as the counterfactual baseline.

    Numeric features use the median; categoricals use the mode. This is the
    same row every contribution comparison starts from, so the per-feature
    deltas are all referenced to the same point."""
    baseline = {}
    for f in NUMERIC_FEATURES:
        baseline[f] = float(df[f].median())
    for f in CATEGORICAL_FEATURES:
        baseline[f] = float(df[f].mode().iloc[0])
    return baseline


def train_and_save() -> dict:
    df = load_dataset()
    X, y = df[FEATURES], df["target"]
    pipe = build_pipeline()
    scores = cross_val_score(pipe, X, y, cv=5, scoring="roc_auc")
    pipe.fit(X, y)
    joblib.dump(pipe, MODEL_PATH)
    joblib.dump(_compute_baseline(df), BASELINE_PATH)
    return {"cv_auc_mean": float(scores.mean()), "cv_auc_std": float(scores.std()), "n_samples": len(df)}


def load_or_train() -> tuple[Pipeline, dict]:
    if os.path.exists(MODEL_PATH) and os.path.exists(BASELINE_PATH):
        return joblib.load(MODEL_PATH), joblib.load(BASELINE_PATH)
    train_and_save()
    return joblib.load(MODEL_PATH), joblib.load(BASELINE_PATH)


def _proba(model: Pipeline, row: dict) -> float:
    X = pd.DataFrame([{f: row.get(f, np.nan) for f in FEATURES}])
    return float(model.predict_proba(X)[0, 1])


def _margin(model: Pipeline, row: dict) -> float:
    """Raw decision function output (log-odds-like). Unbounded — so unlike
    predict_proba, differences stay meaningful when the prediction is
    near 0 or 1."""
    X = pd.DataFrame([{f: row.get(f, np.nan) for f in FEATURES}])
    return float(model.decision_function(X)[0])


def _contributions(model: Pipeline, row: dict, baseline: dict) -> list[dict]:
    """Per-feature contribution via leave-one-out in log-odds space.

    For each feature f:
      * Start from the user's full row.
      * Replace ONLY f with the typical-patient value from ``baseline``.
      * raw_delta = margin(user's row) - margin(row with f replaced).

    Working in margin space avoids the probability-saturation problem: a
    profile predicted at 99.9% will barely move in probability when any
    single feature is flipped, but the log-odds still reflect how much
    each feature is "pushing". Deltas are then normalised to fractions of
    the total absolute contribution, so bars always span a useful range.
    """
    user_margin = _margin(model, row)
    raws = []
    for f in FEATURES:
        if f not in row:
            continue
        probe = dict(row)
        probe[f] = baseline[f]
        raws.append((f, user_margin - _margin(model, probe)))

    total = sum(abs(d) for _, d in raws) or 1.0
    contribs = []
    for f, raw in raws:
        share = raw / total  # in [-1, 1]
        if abs(share) < 0.005:
            continue
        contribs.append({
            "feature": f,
            "label": FEATURE_LABELS.get(f, f),
            "value": row[f],
            "delta": round(share, 4),  # normalised share of the log-odds move
            "raw_logodds_delta": round(raw, 4),
            "direction": "up" if raw > 0 else "down",
        })
    contribs.sort(key=lambda c: abs(c["delta"]), reverse=True)
    return contribs


def predict(model: Pipeline, row: dict, baseline: dict | None = None) -> dict:
    proba = _proba(model, row)
    result = {
        "probability": proba,
        "risk_band": _band(proba),
        "recommendations": _recommendations(row, proba),
    }
    if baseline is not None:
        result["baseline_probability"] = round(_proba(model, baseline), 4)
        result["contributions"] = _contributions(model, row, baseline)
    return result


def _band(p: float) -> str:
    if p < 0.25:
        return "low"
    if p < 0.55:
        return "moderate"
    return "high"


def _recommendations(row: dict, p: float) -> list[str]:
    tips: list[str] = []
    if p >= 0.55:
        tips.append("Discuss these results with a physician — the model flags this profile as high risk.")
    elif p >= 0.25:
        tips.append("Consider a routine cardiovascular check-up in the next 6–12 months.")
    else:
        tips.append("Keep up preventive habits and screen periodically per age-appropriate guidelines.")
    try:
        if float(row.get("trestbps", 0)) >= 140:
            tips.append("Resting BP ≥ 140 mmHg: track daily readings and reduce sodium.")
        if float(row.get("chol", 0)) >= 240:
            tips.append("Cholesterol ≥ 240 mg/dL: discuss lipid panel and diet with your doctor.")
        if int(row.get("fbs", 0)) == 1:
            tips.append("Fasting glucose > 120 mg/dL: request an HbA1c test.")
        if int(row.get("exang", 0)) == 1:
            tips.append("Exercise-induced angina was reported — do not ignore chest pain on exertion.")
        if float(row.get("thalach", 250)) < 100 and int(row.get("age", 0)) < 60:
            tips.append("Max heart rate seems low for your age — confirm the value is from real exercise testing.")
    except (TypeError, ValueError):
        pass
    return tips


if __name__ == "__main__":
    stats = train_and_save()
    print(f"Trained on {stats['n_samples']} samples; 5-fold ROC-AUC = {stats['cv_auc_mean']:.3f} ± {stats['cv_auc_std']:.3f}")
