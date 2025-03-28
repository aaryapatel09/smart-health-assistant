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
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Fade,
  Zoom,
  Slide,
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import axios from 'axios';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#4CAF50',
    },
    secondary: {
      main: '#FF5722',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h3: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 500,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
  },
});

const examplePresets = {
  healthy: {
    name: "Healthy Individual",
    age: 28,
    bmi: 22,
    blood_pressure: 120,
    heart_rate: 72,
    cholesterol: 180,
    glucose: 95,
  },
  heartDisease: {
    name: "Heart Disease Risk",
    age: 55,
    bmi: 28,
    blood_pressure: 145,
    heart_rate: 95,
    cholesterol: 250,
    glucose: 110,
  },
  diabetes: {
    name: "Diabetes Risk",
    age: 45,
    bmi: 32,
    blood_pressure: 130,
    heart_rate: 85,
    cholesterol: 220,
    glucose: 160,
  },
};

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

  const handlePresetSelect = (preset) => {
    setFormData(examplePresets[preset]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // For demo purposes, generate mock results
      const mockResults = {
        disease_probability: Math.random() * 0.3 + 0.1,
        risk_score: Math.random() * 40 + 20,
        recommendations: [
          "Maintain a balanced diet rich in fruits and vegetables",
          "Exercise regularly for at least 30 minutes daily",
          "Get adequate sleep (7-8 hours per night)",
          "Stay hydrated throughout the day",
          "Schedule regular health check-ups",
        ]
      };
      setResults(mockResults);
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
          <Fade in timeout={1000}>
            <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ mb: 2 }}>
              Smart Health Assistant
            </Typography>
          </Fade>
          
          <Fade in timeout={1000} style={{ transitionDelay: '200ms' }}>
            <Typography variant="subtitle1" align="center" color="text.secondary" paragraph>
              Quick health assessment tool - Get instant insights about your health status
            </Typography>
          </Fade>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Slide direction="right" in timeout={1000} style={{ transitionDelay: '400ms' }}>
                <Card>
                  <CardContent>
                    <Typography variant="h5" gutterBottom>
                      Enter Your Health Data
                    </Typography>
                    
                    <FormControl fullWidth sx={{ mb: 3 }}>
                      <InputLabel>Example Presets</InputLabel>
                      <Select
                        label="Example Presets"
                        onChange={(e) => handlePresetSelect(e.target.value)}
                        value=""
                      >
                        <MenuItem value="healthy">Healthy Individual</MenuItem>
                        <MenuItem value="heartDisease">Heart Disease Risk</MenuItem>
                        <MenuItem value="diabetes">Diabetes Risk</MenuItem>
                      </Select>
                    </FormControl>

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
                            sx={{ py: 1.5 }}
                          >
                            {loading ? <CircularProgress size={24} /> : 'Get Health Analysis'}
                          </Button>
                        </Grid>
                      </Grid>
                    </form>
                  </CardContent>
                </Card>
              </Slide>
            </Grid>

            <Grid item xs={12} md={6}>
              <Slide direction="left" in timeout={1000} style={{ transitionDelay: '400ms' }}>
                {error && (
                  <Typography color="error" gutterBottom>
                    {error}
                  </Typography>
                )}
                
                {results && (
                  <Zoom in timeout={1000}>
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

                        <Paper sx={{ p: 2, bgcolor: 'background.default' }}>
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
                  </Zoom>
                )}
              </Slide>
            </Grid>
          </Grid>

          <Fade in timeout={1000} style={{ transitionDelay: '800ms' }}>
            <Box sx={{ mt: 4, textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary" paragraph>
                This tool is for educational purposes only. Always consult a healthcare professional for medical advice.
              </Typography>
              <Link 
                href="https://github.com/aaryapatel09/smart-health-assistant" 
                target="_blank" 
                rel="noopener noreferrer"
                sx={{ 
                  textDecoration: 'none',
                  '&:hover': {
                    textDecoration: 'underline',
                  }
                }}
              >
                View on GitHub
              </Link>
            </Box>
          </Fade>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App; 