import tensorflow as tf
import numpy as np
from sklearn.preprocessing import StandardScaler

class DiseasePredictor:
    def __init__(self):
        self.model = self._build_model()
        self.scaler = StandardScaler()
        
    def _build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(6,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def predict(self, features):
        # Scale features
        scaled_features = self.scaler.fit_transform(features)
        
        # Make prediction
        prediction = self.model.predict(scaled_features)
        return prediction[0][0] 