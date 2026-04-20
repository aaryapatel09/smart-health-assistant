# Smart Health Assistant

Heart disease risk estimator built on the UCI Cleveland dataset (303 patients, 13 features). Trains a gradient-boosted classifier once on first run, then serves predictions through a small Flask API with a single-page frontend.

**Not a medical device.** This is an educational demo trained on a small, biased research cohort.

## Run locally

```bash
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```

First request triggers a one-time training step (~1 s on the Cleveland data) and caches `data/heart_model.joblib`. Delete that file to retrain.

## Train standalone

```bash
python model.py
# prints 5-fold ROC-AUC on the training data
```

## Tests

```bash
pip install pytest
pytest tests/
```

## API

```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"age":63,"sex":1,"cp":4,"trestbps":155,"chol":275,"fbs":1,"restecg":2,"thalach":115,"exang":1,"oldpeak":2.8,"slope":3,"ca":2,"thal":7}'
```

Returns `{"probability": <0..1>, "risk_band": "low|moderate|high", "recommendations": [...]}`.

## Feature reference

| Field | Meaning |
| --- | --- |
| `age` | Age in years |
| `sex` | 1 = male, 0 = female |
| `cp` | Chest-pain type (1 typical angina, 2 atypical, 3 non-anginal, 4 asymptomatic) |
| `trestbps` | Resting blood pressure (mm Hg) |
| `chol` | Serum cholesterol (mg/dL) |
| `fbs` | Fasting blood sugar > 120 mg/dL (1/0) |
| `restecg` | Resting ECG (0 normal, 1 ST-T abnormality, 2 LV hypertrophy) |
| `thalach` | Max heart rate during exercise |
| `exang` | Exercise-induced angina (1/0) |
| `oldpeak` | ST depression induced by exercise |
| `slope` | ST slope (1 up, 2 flat, 3 down) |
| `ca` | Major vessels colored by fluoroscopy (0–3) |
| `thal` | 3 normal, 6 fixed defect, 7 reversible defect |

## Data source

UCI Machine Learning Repository — [Heart Disease dataset](https://archive.ics.uci.edu/ml/datasets/Heart+Disease), processed Cleveland split. Committed verbatim at `data/cleveland.data`.
