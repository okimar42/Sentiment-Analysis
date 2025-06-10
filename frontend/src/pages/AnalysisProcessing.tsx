import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Paper, Typography, Box, CircularProgress, Alert, Button } from '@mui/material';
import { getAnalysisFullDetails } from '../services/api';
import { useNotification } from '../contexts/NotificationContext';

function AnalysisProcessing() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { showProcessingStart, showProcessingComplete } = useNotification();
  const [error, setError] = useState<string>('');
  const [retryCount, setRetryCount] = useState(0);
  const [lastPoll, setLastPoll] = useState<string>('');
  const [lastResponse, setLastResponse] = useState<string>('');
  const [processId, setProcessId] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;

    // Show processing started notification when component mounts
    const notificationProcessId = showProcessingStart('Analysis Processing');
    setProcessId(notificationProcessId);

    let isActive = true;
    const pollInterval = setInterval(async () => {
      if (!isActive) return;
      try {
        setLastPoll(new Date().toLocaleTimeString());
        console.log(`[${new Date().toLocaleTimeString()}] Polling for analysis ${id}...`);
        const result = await getAnalysisFullDetails(id);
        const status = result.analysis?.status || 'unknown';
        setLastResponse(`status: ${status}`);
        console.log(`[${new Date().toLocaleTimeString()}] Response status: ${status}`);
        if (status === 'completed') {
          console.log(`[${new Date().toLocaleTimeString()}] Analysis completed, navigating to results`);
          clearInterval(pollInterval);
          showProcessingComplete('Analysis Processing', notificationProcessId, true);
          navigate(`/analysis/${id}`);
        } else if (status === 'failed') {
          console.log(`[${new Date().toLocaleTimeString()}] Analysis failed`);
          clearInterval(pollInterval);
          showProcessingComplete('Analysis Processing', notificationProcessId, false);
          setError('Analysis failed. Please try again.');
        } else {
          // status is 'pending' or 'processing', keep polling
          setRetryCount((c) => c + 1);
        }
      } catch (err: unknown) {
        console.error('Failed to fetch analysis results', err);
        const errorMessage = err instanceof Error ? err.message : 'Failed to fetch analysis results';
        setError(errorMessage);
        clearInterval(pollInterval);
      }
    }, 3000);

    return () => {
      isActive = false;
      clearInterval(pollInterval);
      // If component unmounts without completing, show a neutral message
      if (processId) {
        showProcessingComplete('Analysis Processing', processId, false);
      }
    };
  }, [id, navigate, retryCount, showProcessingStart, showProcessingComplete, processId]);

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