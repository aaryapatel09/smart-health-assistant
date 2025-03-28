import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class RiskAssessor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self._train_model()
        
    def _train_model(self):
        # Load and prepare data
        data = pd.read_csv('backend/data/health_data.csv')
        X = data.drop('disease_risk', axis=1)
        
        # Calculate risk score based on features
        y = (
            (data['age'] / 100) * 30 +
            (data['bmi'] / 40) * 20 +
            (data['blood_pressure'] / 200) * 20 +
            (data['heart_rate'] / 200) * 10 +
            (data['cholesterol'] / 300) * 10 +
            (data['glucose'] / 200) * 10
        )
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
    def assess_risk(self, features):
        # Scale features
        scaled_features = self.scaler.transform(features)
        
        # Calculate risk score (0-100)
        risk_score = self.model.predict(scaled_features)
        
        # Normalize to 0-100 range
        normalized_score = np.clip(risk_score[0] * 100, 0, 100)
        return normalized_score 