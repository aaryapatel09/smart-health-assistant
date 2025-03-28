import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import ssl
import urllib.request
import os

def download_medical_cost_data():
    """
    Downloads and preprocesses the Medical Cost Personal Dataset.
    Returns a pandas DataFrame with the processed data.
    """
    # URL for the Medical Cost Personal Dataset
    url = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv"
    
    # Create SSL context that ignores certificate verification
    ssl._create_default_https_context = ssl._create_unverified_context
    
    try:
        # Download and read the dataset
        df = pd.read_csv(url)
        
        # Create our health metrics
        health_data = pd.DataFrame({
            'age': df['age'],
            'bmi': df['bmi'],
            'blood_pressure': np.random.normal(120, 15, len(df)),  # Simulated blood pressure
            'heart_rate': np.random.normal(75, 10, len(df)),  # Simulated heart rate
            'cholesterol': np.random.normal(200, 30, len(df)),  # Simulated cholesterol
            'glucose': np.random.normal(100, 15, len(df)),  # Simulated glucose
            'disease_risk': (df['charges'] > df['charges'].mean()).astype(int)  # High medical costs indicate higher risk
        })
        
        # Scale the features
        scaler = StandardScaler()
        features = ['age', 'bmi', 'blood_pressure', 'heart_rate', 'cholesterol', 'glucose']
        health_data[features] = scaler.fit_transform(health_data[features])
        
        # Save the processed dataset
        output_path = os.path.join(os.path.dirname(__file__), 'health_data.csv')
        health_data.to_csv(output_path, index=False)
        print("Dataset downloaded and processed successfully!")
        
        # Print dataset statistics
        print("\nDataset Statistics:")
        print(f"Total samples: {len(health_data)}")
        print(f"Features: {', '.join(features)}")
        print("\nFeature ranges:")
        for feature in features:
            print(f"{feature}: {health_data[feature].min():.2f} to {health_data[feature].max():.2f}")
        
    except Exception as e:
        print(f"Error downloading dataset: {str(e)}")
        print("Using sample data instead...")
        
        # Create a sample dataset if download fails
        np.random.seed(42)
        n_samples = 1000
        
        health_data = pd.DataFrame({
            'age': np.random.normal(45, 15, n_samples),
            'bmi': np.random.normal(25, 5, n_samples),
            'blood_pressure': np.random.normal(120, 15, n_samples),
            'heart_rate': np.random.normal(75, 10, n_samples),
            'cholesterol': np.random.normal(200, 30, n_samples),
            'glucose': np.random.normal(100, 15, n_samples),
            'disease_risk': np.random.binomial(1, 0.3, n_samples)
        })
        
        # Scale the features
        scaler = StandardScaler()
        features = ['age', 'bmi', 'blood_pressure', 'heart_rate', 'cholesterol', 'glucose']
        health_data[features] = scaler.fit_transform(health_data[features])
        
        # Save the sample dataset
        output_path = os.path.join(os.path.dirname(__file__), 'health_data.csv')
        health_data.to_csv(output_path, index=False)
        print("Sample dataset created successfully!")

if __name__ == "__main__":
    download_medical_cost_data() 