from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from models.disease_predictor import DiseasePredictor
from models.risk_assessor import RiskAssessor
from models.recommender import HealthRecommender

app = Flask(__name__)
CORS(app)

# Initialize ML models
disease_predictor = DiseasePredictor()
risk_assessor = RiskAssessor()
health_recommender = HealthRecommender()

@app.route('/api/predict', methods=['POST'])
def predict_health():
    try:
        data = request.get_json()
        
        # Extract features from request
        features = np.array([
            data.get('age', 0),
            data.get('bmi', 0),
            data.get('blood_pressure', 0),
            data.get('heart_rate', 0),
            data.get('cholesterol', 0),
            data.get('glucose', 0)
        ]).reshape(1, -1)
        
        # Get predictions from models
        disease_probability = disease_predictor.predict(features)
        risk_score = risk_assessor.assess_risk(features)
        recommendations = health_recommender.get_recommendations(features, disease_probability, risk_score)
        
        return jsonify({
            'disease_probability': float(disease_probability),
            'risk_score': float(risk_score),
            'recommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000) 