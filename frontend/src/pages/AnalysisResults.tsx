import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Typography,
  Paper,
  CircularProgress,
  Box,
  Grid,
  Button,
  TextField,
  Slider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox,
  TableContainer,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Pagination,
} from '@mui/material';
import {
  PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip,
  LineChart, Line, XAxis, YAxis, CartesianGrid, BarChart, Bar
} from 'recharts';
import { getAnalysisFullDetails, updateSentiment, searchAnalysisResults } from '../services/api';
import type { Analysis, AnalysisSummary, AnalysisResult, BotAnalysis, SentimentByDate, IQDistribution } from '../services/api';
import { debounce } from 'lodash';
import RedditIcon from '@mui/icons-material/Reddit';
import TwitterIcon from '@mui/icons-material/Twitter';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

// Helper to generate a natural language summary (50-150 words)
function generateSummaryText(summary: AnalysisSummary | null, analysis: Analysis | null) {
  if (!summary || !analysis) return 'No summary available.';
  const { total_posts, average_score, sentiment_distribution, sentiment_percentages } = summary;
  const { query } = analysis;
  if (total_posts === 0) return 'No results found for this analysis.';
  const pos = sentiment_distribution.positive;
  const neg = sentiment_distribution.negative;
  const neu = sentiment_distribution.neutral;
  const posPct = sentiment_percentages.positive.toFixed(1);
  const negPct = sentiment_percentages.negative.toFixed(1);
  const neuPct = sentiment_percentages.neutral.toFixed(1);
  const avg = (average_score * 100).toFixed(1);
  let sentimentSummary = `Out of ${total_posts} posts about "${query}", the average sentiment score was ${avg} (on a scale from -100 to 100). `;
  sentimentSummary += `${pos} (${posPct}%) were positive, ${neg} (${negPct}%) were negative, and ${neu} (${neuPct}%) were neutral.`;
  if (average_score > 0.05) {
    sentimentSummary += ' Overall, the sentiment was positive.';
  } else if (average_score < -0.05) {
    sentimentSummary += ' Overall, the sentiment was negative.';
  } else {
    sentimentSummary += ' Overall, the sentiment was neutral.';
  }
  return sentimentSummary;
}

// Helper to check if Twitter is a source
function hasTwitterSource(analysis: Analysis | null) {
  if (!analysis) return false;
  if (Array.isArray(analysis.source)) {
    return analysis.source.includes('twitter');
  }
  return analysis.source === 'twitter';
}

const AnalysisResults = ({ analysisId }: { analysisId?: any }) => {
  const { id } = useParams();
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [summary, setSummary] = useState<AnalysisSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [debugStatus, setDebugStatus] = useState('');
  const [debugFull, setDebugFull] = useState('');
  const [searchParams, setSearchParams] = useState({
    q: '',
    sentiment: 'all',
    sarcasm: null,
    bot: null,
    min_iq: 0,
    sort_by: 'date',
    sort_order: 'desc',
    page: 1,
    page_size: 20
  });
  const [searchResults, setSearchResults] = useState<{ results: AnalysisResult[]; total_count: number; page: number; page_size: number; total_pages: number }>({
    results: [],
    total_count: 0,
    page: 1,
    page_size: 20,
    total_pages: 0
  });
  const [sentimentByDate, setSentimentByDate] = useState<SentimentByDate[]>([]);
  const [iqDistribution, setIQDistribution] = useState<IQDistribution[]>([]);
  const [botAnalysis, setBotAnalysis] = useState<BotAnalysis | null>(null);
  const [editingResult, setEditingResult] = useState<AnalysisResult | null>(null);
  const [editingSentiment, setEditingSentiment] = useState(0);
  const [editingReason, setEditingReason] = useState('');
  // Add state for graph styles
  const [sentimentDistType, setSentimentDistType] = useState('pie');
  const [sentimentOverTimeType, setSentimentOverTimeType] = useState('line');
  const [iqDistType, setIqDistType] = useState('bar');

  // Use inline debounce to avoid dependency warning
  const debouncedSearch = debounce(async (params: Record<string, unknown>) => {
    try {
      const results = await searchAnalysisResults(id, params);
      if (!results || !results.results) {
        return;
      }
      setSearchResults(results);
    } catch (error: unknown) {
      console.error('Search error:', error);
      setSearchResults({
        results: [],
        total_count: 0,
        page: 1,
        page_size: 20,
        total_pages: 0
      });
    }
  }, 300);

  // Update search when params change
  useEffect(() => {
    if (id) {
      debouncedSearch(searchParams);
    }
  }, [searchParams, id]);

  const handleSearchChange = (field: string, value: unknown) => {
    setSearchParams(prev => ({
      ...prev,
      [field]: value,
      page: 1 // Reset to first page on any search change
    }));
  };

  const handlePageChange = (event: React.ChangeEvent<unknown>, newPage: number) => {
    setSearchParams(prev => ({
      ...prev,
      page: newPage
    }));
  };

  const fetchData = useCallback(async () => {
    try {
      const data = await getAnalysisFullDetails(id);
      setDebugFull(JSON.stringify(data));
      setDebugStatus(data.analysis?.status || 'N/A');
      // Set analysis data
      setAnalysis(data.analysis);
      
      // Set summary data
      setSummary(data.summary);
      
      // Process sentiment by date data
      const sentimentData = data.sentiment_by_date.map((item: any) => ({
        date: new Date(item.post_date).toLocaleDateString(),
        score: item.avg_score,
        count: item.count
      }));
      setSentimentByDate(sentimentData);
      
      // Process IQ distribution data
      const iqData = data.iq_distribution.map((item: any) => ({
        iq: item.perceived_iq,
        count: item.count
      }));
      setIQDistribution(iqData);
      
      // Process bot analysis data
      setBotAnalysis(data.bot_analysis);
      
      // Attach results to analysis for filtering
      if (data.results) {
        setAnalysis((prev) => ({ ...prev, results: data.results }));
        // If results exist, stop loading (fallback)
        if (Array.isArray(data.results) && data.results.length > 0) {
          setLoading(false);
        }
      }
      
      // Update processing state based on analysis status
      const newProcessingState = data.analysis.status === 'processing';
      setIsProcessing(newProcessingState);
      
      // If analysis is completed or failed, stop loading
      if (data.analysis.status === 'completed' || data.analysis.status === 'failed') {
        setLoading(false);
      }
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch analysis details';
      setError(errorMessage);
      setLoading(false);
    }
  }, [id]);

  // Initial data fetch
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Polling effect
  useEffect(() => {
    let pollInterval;
    
    const startPolling = () => {
      pollInterval = setInterval(fetchData, 3000);
    };

    const stopPolling = () => {
      if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
      }
    };

    if (isProcessing) {
      startPolling();
    } else {
      stopPolling();
    }

    return () => {
      stopPolling();
    };
  }, [isProcessing, fetchData, id]);

  // Additional effect to check status changes
  useEffect(() => {
    if (analysis && analysis.status === 'completed' && isProcessing) {
      setIsProcessing(false);
    }
  }, [analysis, isProcessing]);

  const handleEditClick = (result) => {
    if (!result.id) {
      return;
    }
    setEditingResult(result);
    setEditingSentiment(typeof result.score === 'number' ? result.score : 0);
    setEditingReason('');
  };

  const handleCancelEdit = () => {
    setEditingResult(null);
    setEditingSentiment(0);
    setEditingReason('');
  };

  const handleSaveEdit = async () => {
    try {
      if (!id || !editingResult?.id) {
        return;
      }
      const updatedResult = await updateSentiment(id, editingResult.id, editingSentiment, editingReason);
      if (!updatedResult) {
        return;
      }
      // Clear editing state
      setEditingResult(null);
      setEditingSentiment(0);
      setEditingReason('');
      // Immediately update the local searchResults state
      setSearchResults((prev) => ({
        ...prev,
        results: prev.results.map((r) =>
          r.id === updatedResult.id ? { ...r, ...updatedResult } : r
        ),
      }));
      // Refetch summary and sentiment-by-date to update graphs
      await fetchData();
    } catch (error: unknown) {
      console.error('Error updating result:', error);
      // Optionally show user-friendly error message
      setError('Failed to update result. Please try again.');
    }
  };

  if (loading) {
    return (
      <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
        <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
          Debug: status = {debugStatus}
        </Typography>
        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
          Debug: full = {debugFull}
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Container>
        <Typography color="error" variant="h6">
          Error: {error}
        </Typography>
      </Container>
    );
  }

  if (isProcessing) {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" minHeight="80vh">
        <CircularProgress />
        <Typography variant="h6" style={{ marginTop: '20px' }}>
          Processing your analysis...
        </Typography>
      </Box>
    );
  }

  const sentimentData = [
    { name: 'Positive', value: summary.sentiment_distribution.positive },
    { name: 'Neutral', value: summary.sentiment_distribution.neutral },
    { name: 'Negative', value: summary.sentiment_distribution.negative },
  ];

  return (
    <Container maxWidth="lg" style={{ marginTop: '2rem' }}>
      <Typography variant="h4" gutterBottom>
        Analysis Results: {analysis.query}
      </Typography>

      {/* Summary and Twitter Grok Summary side by side */}
      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2, mb: 3 }}>
        <Paper sx={{ p: 2, flex: 1, background: '#f5f5f5' }}>
          <Typography variant="h6">Summary</Typography>
          <Typography variant="body1">
            {generateSummaryText(summary, analysis)}
          </Typography>
        </Paper>
        {hasTwitterSource(analysis) && summary && analysis && analysis.twitter_grok_summary && (
          <Paper sx={{ p: 2, flex: 1, background: '#f5f5f5', border: '1px solid #ddd' }}>
            <Typography variant="h6" color="primary">Twitter Grok Summary</Typography>
            <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
              {analysis.twitter_grok_summary}
            </Typography>
          </Paper>
        )}
      </Box>

      <Grid container spacing={3} columns={12}>
        {/* Sentiment Distribution */}
        <Grid columnSpan={{ xs: 12, md: 6 }}>
          <Paper style={{ padding: '20px' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" gutterBottom sx={{ flexGrow: 1 }}>
                Sentiment Distribution
              </Typography>
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Graph</InputLabel>
                <Select
                  value={sentimentDistType}
                  label="Graph"
                  onChange={e => setSentimentDistType(e.target.value)}
                >
                  <MenuItem value="pie">Pie</MenuItem>
                  <MenuItem value="bar">Bar</MenuItem>
                </Select>
              </FormControl>
            </Box>
            {sentimentDistType === 'pie' ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={sentimentData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {sentimentData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={sentimentData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="value" fill="#8884d8">
                    {sentimentData.map((entry, index) => (
                      <Cell key={`cell-bar-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            )}
          </Paper>
        </Grid>

        {/* Sentiment Over Time */}
        <Grid columnSpan={{ xs: 12, md: 6 }}>
          <Paper style={{ padding: '20px' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" gutterBottom sx={{ flexGrow: 1 }}>
                Sentiment Over Time
              </Typography>
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Graph</InputLabel>
                <Select
                  value={sentimentOverTimeType}
                  label="Graph"
                  onChange={e => setSentimentOverTimeType(e.target.value)}
                >
                  <MenuItem value="line">Line</MenuItem>
                  <MenuItem value="bar">Bar</MenuItem>
                </Select>
              </FormControl>
            </Box>
            {sentimentOverTimeType === 'line' ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={sentimentByDate}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="score" stroke="#8884d8" name="Sentiment" />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={sentimentByDate}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="score" fill="#8884d8" name="Sentiment" />
                </BarChart>
              </ResponsiveContainer>
            )}
          </Paper>
        </Grid>

        {/* IQ Distribution */}
        <Grid columnSpan={{ xs: 12, md: 6 }}>
          <Paper style={{ padding: '20px' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" gutterBottom sx={{ flexGrow: 1 }}>
                IQ Distribution
              </Typography>
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Graph</InputLabel>
                <Select
                  value={iqDistType}
                  label="Graph"
                  onChange={e => setIqDistType(e.target.value)}
                >
                  <MenuItem value="bar">Bar</MenuItem>
                  <MenuItem value="pie">Pie</MenuItem>
                </Select>
              </FormControl>
            </Box>
            {iqDistType === 'bar' ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={iqDistribution}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="iq" 
                    label={{ value: 'IQ Score', position: 'insideBottom', offset: -5 }}
                    domain={[55, 145]}
                    ticks={[55, 70, 85, 100, 115, 130, 145]}
                  />
                  <YAxis 
                    label={{ value: 'Number of Posts', angle: -90, position: 'insideLeft' }}
                  />
                  <Tooltip 
                    formatter={(value) => [`${value} posts`, 'Count']}
                    labelFormatter={(label) => `IQ: ${label}`}
                  />
                  <Legend />
                  <Bar dataKey="count" fill="#82ca9d" name="Posts" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={iqDistribution}
                    dataKey="count"
                    nameKey="iq"
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    fill="#82ca9d"
                    label={({ iq, percent }) => `IQ ${iq}: ${(percent * 100).toFixed(0)}%`}
                  >
                    {iqDistribution.map((entry, index) => (
                      <Cell key={`cell-iq-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            )}
          </Paper>
        </Grid>

        {/* Bot Analysis */}
        <Grid columnSpan={{ xs: 12, md: 6 }}>
          <Paper style={{ padding: '20px' }}>
            <Typography variant="h6" gutterBottom>
              Bot Analysis
            </Typography>
            <Typography>Total Posts: {botAnalysis?.total || 0}</Typography>
            <Typography>Detected Bots: {botAnalysis?.bots || 0}</Typography>
            <Typography>Non-Bot Posts: {botAnalysis?.not_bots || 0}</Typography>
            <Typography>Average Bot Probability: {(botAnalysis?.avg_bot_probability * 100 || 0).toFixed(1)}%</Typography>
          </Paper>
        </Grid>

        {/* Search and Filters */}
        <Grid columnSpan={12}>
          <Paper sx={{ p: 2, mb: 2 }}>
            <Grid container spacing={2}>
              {/* Search Input */}
              <Grid columnSpan={{ xs: 12, md: 4 }}>
                <TextField
                  fullWidth
                  label="Search"
                  value={searchParams.q}
                  onChange={(e) => handleSearchChange('q', e.target.value)}
                  placeholder="Search by content..."
                />
              </Grid>

              {/* Sentiment Filter */}
              <Grid columnSpan={{ xs: 12, md: 2 }}>
                <FormControl fullWidth>
                  <InputLabel>Sentiment</InputLabel>
                  <Select
                    value={searchParams.sentiment}
                    onChange={(e) => handleSearchChange('sentiment', e.target.value)}
                    label="Sentiment"
                  >
                    <MenuItem value="all">All</MenuItem>
                    <MenuItem value="positive">Positive</MenuItem>
                    <MenuItem value="negative">Negative</MenuItem>
                    <MenuItem value="neutral">Neutral</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              {/* Sarcasm Filter */}
              <Grid columnSpan={{ xs: 12, md: 2 }}>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={searchParams.sarcasm === true}
                      onChange={(e) => handleSearchChange('sarcasm', e.target.checked)}
                      indeterminate={searchParams.sarcasm === null}
                    />
                  }
                  label="Sarcastic"
                />
              </Grid>

              {/* Bot Filter */}
              <Grid columnSpan={{ xs: 12, md: 2 }}>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={searchParams.bot === true}
                      onChange={(e) => handleSearchChange('bot', e.target.checked)}
                      indeterminate={searchParams.bot === null}
                    />
                  }
                  label="Bots"
                />
              </Grid>

              {/* IQ Filter */}
              <Grid columnSpan={{ xs: 12, md: 2 }}>
                <FormControl fullWidth>
                  <Typography gutterBottom>
                    Min IQ: {searchParams.min_iq}
                  </Typography>
                  <Slider
                    value={searchParams.min_iq}
                    onChange={(e, newValue) => handleSearchChange('min_iq', newValue)}
                    min={0}
                    max={1}
                    step={0.1}
                    valueLabelDisplay="auto"
                  />
                </FormControl>
              </Grid>

              {/* Sort Controls */}
              <Grid columnSpan={{ xs: 12, md: 6 }}>
                <FormControl fullWidth>
                  <InputLabel>Sort By</InputLabel>
                  <Select
                    value={searchParams.sort_by}
                    onChange={(e) => handleSearchChange('sort_by', e.target.value)}
                    label="Sort By"
                  >
                    <MenuItem value="date">Date</MenuItem>
                    <MenuItem value="score">Sentiment Score</MenuItem>
                    <MenuItem value="iq">IQ Score</MenuItem>
                    <MenuItem value="bot_probability">Bot Probability</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid columnSpan={{ xs: 12, md: 6 }}>
                <FormControl fullWidth>
                  <InputLabel>Sort Order</InputLabel>
                  <Select
                    value={searchParams.sort_order}
                    onChange={(e) => handleSearchChange('sort_order', e.target.value)}
                    label="Sort Order"
                  >
                    <MenuItem value="desc">Descending</MenuItem>
                    <MenuItem value="asc">Ascending</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Results Table */}
        <Grid columnSpan={12}>
          <Paper sx={{ p: 2 }}>
            <TableContainer sx={{ overflowX: 'auto' }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell sx={{ wordBreak: 'break-word' }}>Content</TableCell>
                    <TableCell sx={{ wordBreak: 'break-word' }}>Score</TableCell>
                    <TableCell sx={{ wordBreak: 'break-word' }}>Date</TableCell>
                    <TableCell sx={{ wordBreak: 'break-word' }}>IQ</TableCell>
                    <TableCell sx={{ wordBreak: 'break-word' }}>Bot Prob.</TableCell>
                    <TableCell sx={{ wordBreak: 'break-word' }}>Actions</TableCell>
                    <TableCell sx={{ wordBreak: 'break-word' }}>Source</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {searchResults.results && searchResults.results.length > 0 ? (
                    searchResults.results.map((result) => (
                      <TableRow key={result.id}>
                        <TableCell sx={{ wordBreak: 'break-word', maxWidth: 300 }}>{result.content || 'No content'}</TableCell>
                        <TableCell sx={{ wordBreak: 'break-word' }}>
                          {editingResult && editingResult.id === result.id ? (
                            <TextField
                              type="number"
                              value={typeof editingSentiment === 'number' ? (editingSentiment * 100) : 0}
                              onChange={(e) => {
                                const val = parseFloat(e.target.value);
                                setEditingSentiment(isNaN(val) ? 0 : Math.max(-1, Math.min(1, val / 100)));
                              }}
                              inputProps={{ min: -100, max: 100, step: 1 }}
                              size="small"
                            />
                          ) : (
                            typeof result.score === 'number' ? (result.score * 100).toFixed(0) : 0
                          )}
                        </TableCell>
                        <TableCell sx={{ wordBreak: 'break-word' }}>
                          {result.post_date ? new Date(result.post_date).toLocaleString() : 'N/A'}
                        </TableCell>
                        <TableCell sx={{ wordBreak: 'break-word' }}>
                          {typeof result.perceived_iq === 'number' && result.perceived_iq >= 0 ? ((result.perceived_iq * 90 + 55).toFixed(0)) : 'N/A (VADER)'}
                        </TableCell>
                        <TableCell sx={{ wordBreak: 'break-word' }}>
                          {typeof result.bot_probability === 'number' && result.bot_probability >= 0 ? (result.bot_probability * 100).toFixed(1) + '%' : 'N/A (VADER)'}
                        </TableCell>
                        <TableCell sx={{ wordBreak: 'break-word' }}>
                          {editingResult && editingResult.id === result.id ? (
                            <Box sx={{ display: 'flex', gap: 1 }}>
                              <Button
                                size="small"
                                variant="contained"
                                color="primary"
                                onClick={handleSaveEdit}
                                aria-label="Save"
                                data-testid="save-button"
                              >
                                Save
                              </Button>
                              <Button
                                size="small"
                                variant="outlined"
                                onClick={handleCancelEdit}
                              >
                                Cancel
                              </Button>
                            </Box>
                          ) : (
                            <Button
                              size="small"
                              onClick={() => handleEditClick(result)}
                            >
                              Edit
                            </Button>
                          )}
                        </TableCell>
                        <TableCell sx={{ wordBreak: 'break-word' }}>
                          {/* Debug: show the raw value of source_type */}
                          <span style={{ fontSize: 10, color: '#888', marginRight: 4 }}>{result.source_type || 'none'}</span>
                          {result.source_type === 'reddit' && (
                            <Button
                              href={`https://reddit.com/comments/${result.post_id}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              sx={{ minWidth: 0, p: 1, color: '#FF4500', background: 'rgba(255,69,0,0.08)' }}
                            >
                              <RedditIcon />
                            </Button>
                          )}
                          {result.source_type === 'twitter' && (
                            <Button
                              href={`https://twitter.com/i/web/status/${result.post_id}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              sx={{ minWidth: 0, p: 1, color: '#1DA1F2', background: 'rgba(29,161,242,0.08)' }}
                            >
                              <TwitterIcon />
                            </Button>
                          )}
                        </TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableRow>
                      <TableCell colSpan={7} align="center">
                        No results found
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>

            {/* Pagination */}
            {searchResults.total_pages > 1 && (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                <Pagination
                  count={searchResults.total_pages}
                  page={searchResults.page}
                  onChange={handlePageChange}
                  color="primary"
                />
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default AnalysisResults; 