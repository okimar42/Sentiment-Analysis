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
  TableContainer,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Pagination,
  Switch,
} from '@mui/material';
import {
  PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip,
  LineChart, Line, XAxis, YAxis, CartesianGrid, BarChart, Bar
} from 'recharts';
import { getAnalysisFullDetails, searchAnalysisResults } from '../services/api';
import type { Analysis, AnalysisSummary, AnalysisResult, BotAnalysis, SentimentByDate, IQDistribution, SearchParams } from '../services/api';
// Workaround for missing lodash types
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import { debounce } from 'lodash';
import RedditIcon from '@mui/icons-material/Reddit';
import TwitterIcon from '@mui/icons-material/Twitter';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

// Helper functions
const generateSummaryText = (summary: AnalysisSummary | null, analysis: Analysis | null): string => {
  if (!summary || !analysis) return 'No summary available';
  
  const totalPosts = summary.total_posts || 0;
  const avgSentiment = summary.average_score || 0;
  const source = Array.isArray(analysis.source) ? analysis.source.join(', ') : analysis.source;
  
  return `Analysis of ${totalPosts} posts from ${source} shows an average sentiment of ${(avgSentiment * 100).toFixed(1)}%. ` +
    `The sentiment distribution is ${summary.sentiment_distribution.positive}% positive, ` +
    `${summary.sentiment_distribution.neutral}% neutral, and ${summary.sentiment_distribution.negative}% negative.`;
};

const hasTwitterSource = (analysis: Analysis | null): boolean => {
  if (!analysis || !analysis.source) return false;
  return Array.isArray(analysis.source) 
    ? analysis.source.includes('twitter')
    : analysis.source === 'twitter';
};

interface SearchResultsData {
  results: AnalysisResult[];
  total_count: number;
  page: number;
  page_size: number;
  total_pages: number;
}

const AnalysisResults: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [summary, setSummary] = useState<AnalysisSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [debugStatus, setDebugStatus] = useState('');
  const [debugFull, setDebugFull] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResultsData>({
    results: [],
    total_count: 0,
    page: 1,
    page_size: 20,
    total_pages: 0
  });
  const [searchParams, setSearchParams] = useState<SearchParams>({
    q: '',
    sentiment: 'all',
    sarcasm: 'false',
    bot: 'false',
    min_iq: 0,
    page: 1,
    page_size: 20,
    sort_by: 'date',
    sort_order: 'desc',
  });
  const [sentimentByDate, setSentimentByDate] = useState<SentimentByDate[]>([]);
  const [iqDistribution, setIQDistribution] = useState<IQDistribution[]>([]);
  const [botAnalysis, setBotAnalysis] = useState<BotAnalysis | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [editingResult, setEditingResult] = useState<AnalysisResult | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [editingSentiment, setEditingSentiment] = useState(0);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [editingReason, setEditingReason] = useState('');
  const [sentimentDistType, setSentimentDistType] = useState<'pie' | 'bar'>('pie');
  const [sentimentOverTimeType, setSentimentOverTimeType] = useState<'line' | 'bar'>('line');
  const [iqDistType, setIqDistType] = useState<'bar' | 'line'>('bar');

  // Use inline debounce to avoid dependency warning
  const debouncedSearch = debounce(async (params: SearchParams) => {
    if (!id) return;
    try {
      const results = await searchAnalysisResults(id, params);
      console.log('API response from searchAnalysisResults:', results);
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
  }, [searchParams, id, debouncedSearch]);

  const handlePageChange = (event: React.ChangeEvent<unknown>, newPage: number) => {
    setSearchParams(prev => ({
      ...prev,
      page: newPage
    }));
  };

  const fetchData = useCallback(async () => {
    if (!id) return;
    try {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const data: any = await getAnalysisFullDetails(id as string);
      setDebugFull(JSON.stringify(data));
      setDebugStatus(data.analysis?.status || 'N/A');
      setAnalysis(data.analysis);
      setSummary(data.summary);
      
      const sentimentData = data.sentiment_by_date.map((item: SentimentByDate) => ({
        date: new Date(item.post_date).toLocaleDateString(),
        score: item.avg_score,
        count: item.count
      }));
      setSentimentByDate(sentimentData);
      
      const iqData = data.iq_distribution.map((item: IQDistribution) => ({
        iq: item.perceived_iq,
        count: item.count
      }));
      setIQDistribution(iqData);
      
      setBotAnalysis(data.bot_analysis);
      
      if (data.results) {
        setAnalysis((prev) => prev ? { ...prev, results: data.results } : null);
        if (Array.isArray(data.results) && data.results.length > 0) {
          setLoading(false);
        }
      }
      
      const newProcessingState = data.analysis.status === 'processing';
      setIsProcessing(newProcessingState);
      
      if (data.analysis.status === 'completed' || data.analysis.status === 'failed') {
        setLoading(false);
      }
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch analysis details';
      setError(errorMessage);
      setLoading(false);
    }
  }, [id]);

  // Only fetch analysis details when id changes
  useEffect(() => {
    fetchData();
  }, [fetchData, id]);

  // Only search when searchParams changes
  // The dependency array is intentionally limited to avoid excessive searches
  useEffect(() => {
    if (id) {
      debouncedSearch(searchParams);
    }
  }, [searchParams, id, debouncedSearch]);

  // Polling effect
  useEffect(() => {
    let pollInterval: NodeJS.Timeout | undefined;
    
    const startPolling = () => {
      pollInterval = setInterval(fetchData, 3000);
    };

    const stopPolling = () => {
      if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = undefined;
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
  }, [isProcessing, fetchData]);

  const handleEditClick = (result: AnalysisResult) => {
    if (!result.id) return;
    setEditingResult(result);
    setEditingSentiment(typeof result.score === 'number' ? result.score : 0);
    setEditingReason('');
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

  if (!summary || !analysis) {
    return (
      <Container>
        <Typography color="error" variant="h6">
          No analysis data available
        </Typography>
      </Container>
    );
  }

  const sentimentData = [
    { name: 'Positive', value: summary.sentiment_distribution.positive },
    { name: 'Neutral', value: summary.sentiment_distribution.neutral },
    { name: 'Negative', value: summary.sentiment_distribution.negative },
  ];

  // Add debug log before rendering the table
  console.log('Rendering table, searchResults.results:', searchResults.results);

  return (
    <Container maxWidth="lg" style={{ marginTop: '2rem' }}>
      <Typography variant="h4" gutterBottom>
        Analysis Results: {analysis.query}
      </Typography>

      {/* Summary and Twitter Grok Summary side by side */}
      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2, mb: 3 }}>
        <Paper sx={{ p: 2, flex: 1, bgcolor: 'background.paper', color: 'text.primary' }}>
          <Typography variant="h6">Summary</Typography>
          <Typography variant="body1">
            {generateSummaryText(summary, analysis)}
          </Typography>
        </Paper>
        {hasTwitterSource(analysis) && analysis.twitter_grok_summary && (
          <Paper sx={{ p: 2, flex: 1, bgcolor: 'background.paper', color: 'text.primary', border: 1, borderColor: 'divider' }}>
            <Typography variant="h6" color="primary">Twitter Grok Summary</Typography>
            <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
              {analysis.twitter_grok_summary}
            </Typography>
          </Paper>
        )}
      </Box>

      <Grid container spacing={3}>
        {/* Sentiment Distribution */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Sentiment Distribution
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Graph</InputLabel>
                <Select
                  value={String(sentimentDistType)}
                  onChange={(e) => setSentimentDistType(e.target.value as 'pie' | 'bar')}
                  label="Graph"
                >
                  <MenuItem value="pie">Pie Chart</MenuItem>
                  <MenuItem value="bar">Bar Chart</MenuItem>
                </Select>
              </FormControl>
            </Box>
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                {sentimentDistType === 'pie' ? (
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
                ) : (
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
                )}
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>

        {/* Sentiment Over Time */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Sentiment Over Time
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Graph</InputLabel>
                <Select
                  value={String(sentimentOverTimeType)}
                  onChange={(e) => setSentimentOverTimeType(e.target.value as 'line' | 'bar')}
                  label="Graph"
                >
                  <MenuItem value="line">Line Chart</MenuItem>
                  <MenuItem value="bar">Bar Chart</MenuItem>
                </Select>
              </FormControl>
            </Box>
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                {sentimentOverTimeType === 'line' ? (
                  <LineChart data={sentimentByDate}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="score" stroke="#8884d8" />
                  </LineChart>
                ) : (
                  <BarChart data={sentimentByDate}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="score" fill="#8884d8" />
                  </BarChart>
                )}
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>

        {/* IQ Distribution */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              IQ Distribution
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Graph</InputLabel>
                <Select
                  value={String(iqDistType)}
                  onChange={(e) => setIqDistType(e.target.value as 'bar' | 'line')}
                  label="Graph"
                >
                  <MenuItem value="bar">Bar Chart</MenuItem>
                  <MenuItem value="line">Line Chart</MenuItem>
                </Select>
              </FormControl>
            </Box>
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                {iqDistType === 'bar' ? (
                  <BarChart data={iqDistribution}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="iq" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="count" fill="#8884d8" />
                  </BarChart>
                ) : (
                  <LineChart data={iqDistribution}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="iq" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="count" stroke="#8884d8" />
                  </LineChart>
                )}
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>

        {/* Bot Analysis */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Bot Analysis
            </Typography>
            {botAnalysis && (
              <Box>
                <Typography variant="body1">
                  Average Bot Probability: {(botAnalysis.avg_bot_probability || 0).toFixed(2)}
                </Typography>
                <Typography variant="body1">
                  Total Posts: {botAnalysis.total}
                </Typography>
                <Typography variant="body1">
                  Bot Posts: {botAnalysis.bots}
                </Typography>
                <Typography variant="body1">
                  Human Posts: {botAnalysis.not_bots}
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Search and Filters */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Grid container spacing={2}>
              {/* Search Input */}
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  label="Search"
                  value={searchParams.q}
                  onChange={(e) => setSearchParams(prev => ({ ...prev, q: e.target.value }))}
                  placeholder="Search by content..."
                />
              </Grid>

              {/* Sentiment Filter */}
              <Grid item xs={12} md={2}>
                <FormControl fullWidth>
                  <InputLabel>Sentiment</InputLabel>
                  <Select
                    value={String(searchParams.sentiment)}
                    onChange={(e) => setSearchParams(prev => ({ ...prev, sentiment: String(e.target.value) }))}
                    label="Sentiment"
                  >
                    <MenuItem value="all">All</MenuItem>
                    <MenuItem value="positive">Positive</MenuItem>
                    <MenuItem value="neutral">Neutral</MenuItem>
                    <MenuItem value="negative">Negative</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              {/* Sarcasm Filter */}
              <Grid item xs={12} md={2}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={searchParams.sarcasm === 'true'}
                      onChange={(e) => setSearchParams(prev => ({ ...prev, sarcasm: e.target.checked ? 'true' : 'false' }))}
                      color="primary"
                    />
                  }
                  label="Sarcastic"
                />
              </Grid>

              {/* Bot Filter */}
              <Grid item xs={12} md={2}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={searchParams.bot === 'true'}
                      onChange={(e) => setSearchParams(prev => ({ ...prev, bot: e.target.checked ? 'true' : 'false' }))}
                      color="primary"
                    />
                  }
                  label="Bot"
                />
              </Grid>

              {/* IQ Filter */}
              <Grid item xs={12} md={2}>
                <Typography gutterBottom>Min IQ: {Number(searchParams.min_iq).toFixed(2)}</Typography>
                <Slider
                  value={typeof searchParams.min_iq === 'number' ? searchParams.min_iq : Number(searchParams.min_iq) || 0}
                  onChange={(_e, newValue) => setSearchParams(prev => ({ ...prev, min_iq: typeof newValue === 'number' ? newValue : (Array.isArray(newValue) ? newValue[0] : 0) }))}
                  min={0}
                  max={1}
                  step={0.01}
                  marks
                  valueLabelDisplay="auto"
                />
              </Grid>

              {/* Sort Controls */}
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Sort By</InputLabel>
                  <Select
                    value={String(searchParams.sort_by)}
                    onChange={(e) => setSearchParams(prev => ({ ...prev, sort_by: String(e.target.value) }))}
                    label="Sort By"
                  >
                    <MenuItem value="date">Date</MenuItem>
                    <MenuItem value="sentiment">Sentiment</MenuItem>
                    <MenuItem value="iq">IQ</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Sort Order</InputLabel>
                  <Select
                    value={String(searchParams.sort_order)}
                    onChange={(e) => setSearchParams(prev => ({ ...prev, sort_order: String(e.target.value) }))}
                    label="Sort Order"
                  >
                    <MenuItem value="asc">Ascending</MenuItem>
                    <MenuItem value="desc">Descending</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Results Table */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Results
            </Typography>
            <TableContainer sx={{ overflowX: 'auto' }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Source</TableCell>
                    <TableCell>Content</TableCell>
                    <TableCell>Sentiment</TableCell>
                    <TableCell>IQ</TableCell>
                    <TableCell>Bot Probability</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {searchResults.results.map((result) => (
                    <TableRow key={result.id}>
                      <TableCell>
                        {result.source_type === 'reddit' ? <RedditIcon /> : <TwitterIcon />}
                      </TableCell>
                      <TableCell>{result.content}</TableCell>
                      <TableCell>{result.score}</TableCell>
                      <TableCell>{result.perceived_iq}</TableCell>
                      <TableCell>{result.bot_probability}</TableCell>
                      <TableCell>
                        <Button
                          variant="outlined"
                          size="small"
                          onClick={() => handleEditClick(result)}
                        >
                          Edit
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
              <Pagination
                count={searchResults.total_pages || 1}
                page={searchParams.page || 1}
                onChange={handlePageChange}
                color="primary"
              />
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default AnalysisResults; 