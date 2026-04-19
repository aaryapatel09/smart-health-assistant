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

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "data", "cleveland.data")
MODEL_PATH = os.path.join(HERE, "data", "heart_model.joblib")


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, header=None, names=COLUMNS, na_values="?")
    df["target"] = (df["num"] > 0).astype(int)
    return df


def build_pipeline() -> Pipeline:
    numeric = ["age", "trestbps", "chol", "thalach", "oldpeak"]
    categorical = ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"]
    preproc = ColumnTransformer([
        ("num", Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]), numeric),
        ("cat", Pipeline([
            ("impute", SimpleImputer(strategy="most_frequent")),
        ]), categorical),
    ])
    return Pipeline([
        ("pre", preproc),
        ("clf", GradientBoostingClassifier(n_estimators=200, max_depth=3, random_state=42)),
    ])


def train_and_save() -> dict:
    df = load_dataset()
    X, y = df[FEATURES], df["target"]
    pipe = build_pipeline()
    scores = cross_val_score(pipe, X, y, cv=5, scoring="roc_auc")
    pipe.fit(X, y)
    joblib.dump(pipe, MODEL_PATH)
    return {"cv_auc_mean": float(scores.mean()), "cv_auc_std": float(scores.std()), "n_samples": len(df)}


def load_or_train() -> Pipeline:
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    train_and_save()
    return joblib.load(MODEL_PATH)


def predict(model: Pipeline, row: dict) -> dict:
    X = pd.DataFrame([{f: row.get(f, np.nan) for f in FEATURES}])
    proba = float(model.predict_proba(X)[0, 1])
    return {
        "probability": proba,
        "risk_band": _band(proba),
        "recommendations": _recommendations(row, proba),
    }


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
