import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Button,
} from '@mui/material';
import { getAnalysis, type Analysis } from '../services/analysis.api';

function Results() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchResults = async () => {
      if (!id) {
        setError('No analysis ID provided');
        setLoading(false);
        return;
      }

      try {
        const data = await getAnalysis(id);
        console.log('Analysis data:', data); // Debug log
        setAnalysis(data);
      } catch (err) {
        console.error('Error fetching analysis:', err); // Debug log
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [id]);

  if (loading) {
    return (
      <Container maxWidth="md" sx={{ mt: 4, textAlign: 'center' }}>
        <CircularProgress />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Loading analysis results...
        </Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>
        <Button variant="contained" onClick={() => navigate('/')}>
          Back to Dashboard
        </Button>
      </Container>
    );
  }

  if (!analysis) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="warning" sx={{ mb: 2 }}>No results found</Alert>
        <Button variant="contained" onClick={() => navigate('/')}>
          Back to Dashboard
        </Button>
      </Container>
    );
  }

  if (analysis.status === 'processing') {
    return (
      <Container maxWidth="md" sx={{ mt: 4, textAlign: 'center' }}>
        <CircularProgress />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Analysis is still processing...
        </Typography>
        <Button variant="contained" sx={{ mt: 2 }} onClick={() => navigate('/')}>
          Back to Dashboard
        </Button>
      </Container>
    );
  }

  if (analysis.status === 'failed') {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>Analysis failed</Alert>
        <Button variant="contained" onClick={() => navigate('/')}>
          Back to Dashboard
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography variant="h4" component="h1">
            Analysis Results
          </Typography>
          <Button variant="outlined" onClick={() => navigate('/')}>
            Back to Dashboard
          </Button>
        </Box>

        <Box sx={{ mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Query
          </Typography>
          <Typography>{analysis.query}</Typography>
        </Box>

        <Box sx={{ mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Details
          </Typography>
          <Typography>Source: {Array.isArray(analysis.source) ? analysis.source.join(', ') : analysis.source}</Typography>
          <Typography>Model: {analysis.model}</Typography>
          <Typography>Created: {new Date(analysis.created_at).toLocaleString()}</Typography>
        </Box>

        {analysis.results && analysis.results.length > 0 ? (
          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              Results ({analysis.results.length} items)
            </Typography>
            {analysis.results.map((result, index) => (
              <Paper key={index} sx={{ p: 2, mb: 2, bgcolor: 'background.default' }}>
                <Typography variant="subtitle1" gutterBottom>
                  Content:
                </Typography>
                <Typography sx={{ mb: 1 }}>{result.content}</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                  <Typography variant="body2">Score: {result.score.toFixed(2)}</Typography>
                  {result.post_date && (
                    <Typography variant="body2">
                      Date: {new Date(result.post_date).toLocaleString()}
                    </Typography>
                  )}
                  <Typography variant="body2">IQ: {result.perceived_iq.toFixed(1)}</Typography>
                  <Typography variant="body2">
                    Bot Probability: {(result.bot_probability * 100).toFixed(1)}%
                  </Typography>
                </Box>
              </Paper>
            ))}
          </Box>
        ) : (
          <Alert severity="info" sx={{ mb: 4 }}>
            No results available for this analysis.
          </Alert>
        )}

        {analysis.twitter_grok_summary && (
          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              Summary
            </Typography>
            <Typography>{analysis.twitter_grok_summary}</Typography>
          </Box>
        )}
      </Paper>
    </Container>
  );
}

export default Results; 