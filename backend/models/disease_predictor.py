import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class DiseasePredictor:
    def __init__(self):
        self.model = self._build_model()
        self.scaler = StandardScaler()
        self._train_model()
        
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
    
    def _train_model(self):
        # Load and prepare data
        data = pd.read_csv('backend/data/health_data.csv')
        X = data.drop('disease_risk', axis=1)
        y = data['disease_risk']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(
            X_train_scaled, y_train,
            epochs=50,
            batch_size=4,
            validation_data=(X_test_scaled, y_test),
            verbose=0
        )
    
    def predict(self, features):
        # Scale features
        scaled_features = self.scaler.transform(features)
        
        # Make prediction
        prediction = self.model.predict(scaled_features)
        return prediction[0][0] 