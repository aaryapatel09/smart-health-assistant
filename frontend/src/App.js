import React, { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Paper,
  Link,
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import axios from 'axios';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#f50057',
    },
  },
});

function App() {
  const [formData, setFormData] = useState({
    age: '',
    bmi: '',
    blood_pressure: '',
    heart_rate: '',
    cholesterol: '',
    glucose: '',
  });
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/predict', formData);
      setResults(response.data);
    } catch (err) {
      setError('Error getting predictions. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            Smart Health Assistant
          </Typography>
          
          <Typography variant="subtitle1" align="center" color="text.secondary" paragraph>
            Quick health assessment tool - Get instant insights about your health status
          </Typography>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    Enter Your Health Data
                  </Typography>
                  <form onSubmit={handleSubmit}>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          fullWidth
                          label="Age"
                          name="age"
                          type="number"
                          value={formData.age}
                          onChange={handleChange}
                          required
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          fullWidth
                          label="BMI"
                          name="bmi"
                          type="number"
                          value={formData.bmi}
                          onChange={handleChange}
                          required
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          fullWidth
                          label="Blood Pressure"
                          name="blood_pressure"
                          type="number"
                          value={formData.blood_pressure}
                          onChange={handleChange}
                          required
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          fullWidth
                          label="Heart Rate"
                          name="heart_rate"
                          type="number"
                          value={formData.heart_rate}
                          onChange={handleChange}
                          required
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          fullWidth
                          label="Cholesterol"
                          name="cholesterol"
                          type="number"
                          value={formData.cholesterol}
                          onChange={handleChange}
                          required
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          fullWidth
                          label="Glucose"
                          name="glucose"
                          type="number"
                          value={formData.glucose}
                          onChange={handleChange}
                          required
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <Button
                          fullWidth
                          variant="contained"
                          color="primary"
                          type="submit"
                          disabled={loading}
                        >
                          {loading ? <CircularProgress size={24} /> : 'Get Health Analysis'}
                        </Button>
                      </Grid>
                    </Grid>
                  </form>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              {error && (
                <Typography color="error" gutterBottom>
                  {error}
                </Typography>
              )}
              
              {results && (
                <Card>
                  <CardContent>
                    <Typography variant="h5" gutterBottom>
                      Health Analysis Results
                    </Typography>
                    
                    <Box sx={{ mb: 3 }}>
                      <Typography variant="h6" gutterBottom>
                        Disease Risk Probability
                      </Typography>
                      <Typography variant="h4" color="primary">
                        {(results.disease_probability * 100).toFixed(1)}%
                      </Typography>
                    </Box>

                    <Box sx={{ mb: 3 }}>
                      <Typography variant="h6" gutterBottom>
                        Overall Health Risk Score
                      </Typography>
                      <Typography variant="h4" color="secondary">
                        {results.risk_score.toFixed(1)}
                      </Typography>
                    </Box>

                    <Paper sx={{ p: 2 }}>
                      <Typography variant="h6" gutterBottom>
                        Personalized Recommendations
                      </Typography>
                      <List>
                        {results.recommendations.map((rec, index) => (
                          <ListItem key={index}>
                            <ListItemText primary={rec} />
                          </ListItem>
                        ))}
                      </List>
                    </Paper>
                  </CardContent>
                </Card>
              )}
            </Grid>
          </Grid>

          <Box sx={{ mt: 4, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              This tool is for educational purposes only. Always consult a healthcare professional for medical advice.
            </Typography>
            <Link href="https://github.com/aaryapatel09/smart-health-assistant" target="_blank" rel="noopener noreferrer">
              View on GitHub
            </Link>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App; 