import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Paper, Typography, Box, CircularProgress, Alert, Button } from '@mui/material';
import { getAnalysisResults as originalGetAnalysisResults } from '../services/api';
import type { AnalysisResult } from '../services/api';

function getAnalysisResultsNoCache(id: string) {
  // Add a cache-busting query param
  return originalGetAnalysisResults(id + '?_=' + Date.now());
}

function AnalysisProcessing() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [error, setError] = useState<string>('');
  const [retryCount, setRetryCount] = useState<number>(0);
  const [lastPoll, setLastPoll] = useState<string | null>(null);
  const [lastResponse, setLastResponse] = useState<string | null>(null);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (id) {
      interval = setInterval(async () => {
        try {
          const results = await getAnalysisResultsNoCache(id);
          setLastPoll(new Date().toLocaleTimeString());
          setLastResponse(JSON.stringify(results));
          // Handle new backend status response
          if (Array.isArray(results)) {
            if (results.length > 0) {
              navigate(`/analysis/${id}`);
            } else {
              setError('Analysis completed but no results found.');
              clearInterval(interval);
            }
          } else if (results && Array.isArray(results.results)) {
            if (results.results.length > 0) {
              navigate(`/analysis/${id}`);
            } else {
              setError('Analysis completed but no results found.');
              clearInterval(interval);
            }
          } else if (results && results.status) {
            if (results.status === 'failed') {
              setError('Analysis failed. Please try again.');
              clearInterval(interval);
            } // else keep polling for 'pending' or 'processing'
          } else {
            setRetryCount((c) => c + 1);
          }
        } catch (err: unknown) {
          console.error('Failed to fetch analysis results', err);
          const errorMessage = err instanceof Error ? err.message : 'Failed to fetch analysis results';
          setError(errorMessage);
          clearInterval(interval);
        }
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [id, navigate]);

  if (!id) {
    return (
      <Container maxWidth="sm">
        <Box sx={{ mt: 8 }}>
          <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
            <Typography variant="h5" gutterBottom>
              Error: No analysis ID provided.
            </Typography>
            <Button sx={{ mt: 2 }} onClick={() => navigate('/')}>Back to Dashboard</Button>
          </Paper>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8 }}>
        <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h5" gutterBottom>
            Your analysis is being processed...
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
            Debug: id = {id}
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
            Last poll: {lastPoll || 'N/A'}
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
            Last response: {lastResponse || 'N/A'}
          </Typography>
          <CircularProgress sx={{ my: 2 }} />
          <Typography variant="body1" sx={{ mt: 2 }}>
            This may take a few moments. The page will update automatically when results are ready.
          </Typography>
          {retryCount > 10 && (
            <Alert severity="info" sx={{ mt: 2 }}>
              Still processing... If this takes too long, you can check back later from the dashboard.
            </Alert>
          )}
          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>
          )}
          <Button sx={{ mt: 2 }} onClick={() => navigate('/')}>Back to Dashboard</Button>
        </Paper>
      </Box>
    </Container>
  );
}

export default AnalysisProcessing; 