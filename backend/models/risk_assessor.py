import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

class RiskAssessor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        
    def assess_risk(self, features):
        # Scale features
        scaled_features = self.scaler.fit_transform(features)
        
        # Calculate risk score (0-100)
        risk_score = self.model.predict(scaled_features)
        
        # Normalize to 0-100 range
        normalized_score = np.clip(risk_score[0] * 100, 0, 100)
        return normalized_score 