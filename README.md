# Smart Health Assistant 🏥

An AI-powered health prediction and recommendation system that helps users understand their health status and receive personalized recommendations.

## Features

- Health condition prediction using multiple ML models
- Personalized health recommendations
- Modern web interface
- Real-time health insights
- User-friendly dashboard
- Data visualization of health metrics

## Tech Stack

- Python 3.8+
- Flask (Backend)
- React (Frontend)
- Scikit-learn (ML Models)
- TensorFlow (Deep Learning)
- Pandas (Data Processing)
- Plotly (Data Visualization)

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```
4. Run the application:
   ```bash
   # Terminal 1 - Backend
   python app.py
   
   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

## Project Structure

```
smart-health-assistant/
├── backend/
│   ├── models/
│   ├── data/
│   └── app.py
├── frontend/
│   ├── src/
│   └── public/
├── requirements.txt
└── README.md
```

## ML Models Used

1. Disease Prediction Model
2. Health Risk Assessment Model
3. Recommendation Engine

## Contributing

Feel free to submit issues and enhancement requests! 