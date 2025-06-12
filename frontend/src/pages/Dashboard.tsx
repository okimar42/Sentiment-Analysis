import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
  Box,
  CircularProgress,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { getAnalyses } from '../services/analysis.api';
import type { Analysis } from '../services/analysis.api';
import Grid from '@mui/material/Grid';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    fetchAnalyses();
  }, []);

  const fetchAnalyses = async (): Promise<void> => {
    try {
      const data = await getAnalyses();
      setAnalyses(data);
    } catch (err: unknown) {
      console.error('Failed to fetch analyses:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch analyses';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ mt: 4, mb: 4 }}>
          <Paper sx={{ p: 4, bgcolor: 'error.light', mb: 2 }}>
            <Typography color="error" variant="h5">{error}</Typography>
          </Paper>
          <Button variant="contained" color="primary" onClick={() => navigate('/new-analysis')}>
            New Analysis
          </Button>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Grid container spacing={3} columns={12}>
          <Grid item xs={12}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
              <Typography variant="h4" component="h1">
                Recent Analyses
              </Typography>
              <Button
                variant="contained"
                color="primary"
                startIcon={<AddIcon />}
                onClick={() => navigate('/new-analysis')}
              >
                New Analysis
              </Button>
            </Box>
          </Grid>
          {analyses.length === 0 ? (
            <Grid item xs={12}>
              <Paper sx={{ p: 4, textAlign: 'center' }}>
                <Typography variant="h6" color="textSecondary">
                  No analyses found. Start by creating a new analysis.
                </Typography>
              </Paper>
            </Grid>
          ) : (
            analyses.map((analysis) => (
              <Grid item xs={12} md={6} lg={4} key={analysis.id}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      {analysis.query}
                    </Typography>
                    <Typography color="textSecondary" gutterBottom>
                      Source: {analysis.source}
                    </Typography>
                    <Typography color="textSecondary" gutterBottom>
                      Model: {analysis.model}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Created: {new Date(analysis.created_at).toLocaleDateString()}
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button
                      size="small"
                      color="primary"
                      onClick={() => {
                        if (analysis.id) {
                          navigate(`/results/${analysis.id}`);
                        } else {
                          alert('Invalid analysis: missing ID');
                        }
                      }}
                    >
                      View Results
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))
          )}
        </Grid>
      </Box>
    </Container>
  );
}

const DashboardWithBoundary: React.FC = () => {
  try {
    return <Dashboard />;
  } catch {
    return (
      <Container maxWidth="lg">
        <Box sx={{ mt: 4, mb: 4 }}>
          <Paper sx={{ p: 4, bgcolor: 'error.light', mb: 2 }}>
            <Typography color="error" variant="h5">An unexpected error occurred.</Typography>
          </Paper>
        </Box>
      </Container>
    );
  }
}

export default DashboardWithBoundary; 