import numpy as np

class HealthRecommender:
    def __init__(self):
        self.recommendations = {
            'high_risk': [
                "Schedule a comprehensive health check-up",
                "Consult with a healthcare provider",
                "Start a regular exercise routine",
                "Monitor blood pressure daily",
                "Follow a heart-healthy diet"
            ],
            'medium_risk': [
                "Increase physical activity",
                "Maintain a balanced diet",
                "Get adequate sleep",
                "Practice stress management",
                "Stay hydrated"
            ],
            'low_risk': [
                "Continue healthy lifestyle habits",
                "Regular health screenings",
                "Stay active and engaged",
                "Maintain social connections",
                "Practice preventive care"
            ]
        }
    
    def get_recommendations(self, features, disease_probability, risk_score):
        # Determine risk level
        if risk_score >= 70:
            risk_level = 'high_risk'
        elif risk_score >= 40:
            risk_level = 'medium_risk'
        else:
            risk_level = 'low_risk'
        
        # Get base recommendations
        recommendations = self.recommendations[risk_level].copy()
        
        # Add personalized recommendations based on features
        if features[0][0] > 60:  # Age
            recommendations.append("Schedule regular senior health check-ups")
        
        if features[0][1] > 30:  # BMI
            recommendations.append("Consider consulting a nutritionist")
        
        if features[0][2] > 140:  # Blood Pressure
            recommendations.append("Monitor blood pressure regularly")
        
        if features[0][3] > 100:  # Heart Rate
            recommendations.append("Practice stress-reduction techniques")
        
        if features[0][4] > 200:  # Cholesterol
            recommendations.append("Focus on heart-healthy diet choices")
        
        if features[0][5] > 126:  # Glucose
            recommendations.append("Monitor blood sugar levels regularly")
        
        return recommendations 