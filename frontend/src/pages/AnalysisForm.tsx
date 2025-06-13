import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Autocomplete,
  Checkbox,
  ListItemText,
  FormControlLabel,
  Grid,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { createAnalysis } from '../services/analysis.api';
import type { SelectChangeEvent } from '@mui/material/Select';

const SOURCES = [
  { value: 'reddit', label: 'Reddit' },
  { value: 'twitter', label: 'Twitter' },
];

const MODELS = [
  { value: 'vader', label: 'VADER' },
  { value: 'gpt-4', label: 'GPT-4' },
  { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' },
  { value: 'claude-3-opus', label: 'Claude 3 Opus' },
  { value: 'claude-3-sonnet', label: 'Claude 3 Sonnet' },
  { value: 'claude-3-haiku', label: 'Claude 3 Haiku' },
  { value: 'mistral-large', label: 'Mistral Large' },
  { value: 'mistral-medium', label: 'Mistral Medium' },
  { value: 'mistral-small', label: 'Mistral Small' },
  { value: 'mixtral-8x7b', label: 'Mixtral 8x7B' },
  { value: 'llama-2-70b', label: 'Llama 2 70B' },
  { value: 'llama-2-13b', label: 'Llama 2 13B' },
  { value: 'llama-2-7b', label: 'Llama 2 7B' },
  { value: 'gemma-7b', label: 'Gemma 7B' },
  { value: 'gemma-2b', label: 'Gemma 2B' }
];

const ANALYSIS_FEATURES = [
  { value: 'sarcasm', label: 'Sarcasm Detection' },
  { value: 'iq', label: 'IQ Analysis' },
  { value: 'bot', label: 'Bot Detection' },
];

const POPULAR_SUBREDDITS = [
  'wallstreetbets',
  'stocks',
  'investing',
  'stockmarket',
  'finance',
  'personalfinance',
  'options',
  'cryptocurrency',
  'crypto',
  'bitcoin',
  'ethereum',
  'trading',
  'daytrading',
  'forex',
  'dividends',
];

// Helper to get today and yesterday
const today = new Date();
const yesterday = new Date();
yesterday.setDate(today.getDate() - 1);

interface FormData {
  query: string;
  source: string[];
  model: string;
  subreddits: string[];
  start_date: Date | null;
  end_date: Date | null;
  include_images: boolean;
  selected_llms: string[];
  selected_features: string[];
}

function AnalysisForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<FormData>({
    query: '',
    source: ['reddit'],
    model: 'vader',
    subreddits: POPULAR_SUBREDDITS,
    start_date: yesterday,
    end_date: today,
    include_images: false,
    selected_llms: ['vader'],
    selected_features: []
  });
  const [error, setError] = useState<string>('');
  const [customSubreddit, setCustomSubreddit] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | { name?: string; value: unknown }>) => {
    const { name, value } = e.target;
    if (name === 'source') {
      setFormData({
        ...formData,
        source: Array.isArray(value) ? (value as string[]) : typeof value === 'string' ? value.split(',') : [],
      });
    } else if (typeof name === 'string') {
      setFormData({
        ...formData,
        [name]: value as string | string[] | boolean | Date,
      });
    }
  };

  const handleSubredditChange = (event: React.SyntheticEvent, newValue: string[]) => {
    setFormData({
      ...formData,
      subreddits: newValue,
    });
  };

  const handleCustomSubredditAdd = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && customSubreddit) {
      e.preventDefault();
      if (!formData.subreddits.includes(customSubreddit)) {
        setFormData({
          ...formData,
          subreddits: [...formData.subreddits, customSubreddit],
        });
      }
      setCustomSubreddit('');
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    
    // Validation: Require a non-empty query
    if (!formData.query || formData.query.trim() === '') {
      setError('Please enter a search query');
      return;
    }
    
    // Validation: Require at least one model selected
    if (!formData.selected_llms || formData.selected_llms.length === 0) {
      setError('Please select at least one model');
      return;
    }
    
    // Validation: Start date must be before end date
    if (formData.start_date && formData.end_date && formData.start_date > formData.end_date) {
      setError('Start date must be before end date');
      return;
    }
    
    // Validation: Require start and end dates
    if (!formData.start_date || !formData.end_date) {
      setError('Start and end dates are required');
      return;
    }
    
    // Use fallback to formData.model if selected_llms is empty, with hardcoded fallback
    const selectedModels = formData.selected_llms.length > 0 ? formData.selected_llms : [formData.model];
    if (selectedModels.length === 0 || !selectedModels[0]) {
      setError('Please select at least one model');
      return;
    }
    
    try {
      // Ensure we're using VADER if it's selected
      const selectedModel = formData.selected_llms.includes('vader') ? 'vader' : selectedModels[0];
      
      const payload = {
        query: formData.query,
        source: formData.source,
        model: selectedModel.toLowerCase(),
        subreddits: formData.subreddits,
        start_date: formData.start_date!.toISOString(),
        end_date: formData.end_date!.toISOString(),
        include_images: formData.include_images,
        selected_llms: selectedModels.map(model => model.toLowerCase()),
        selected_features: formData.selected_features,
        enable_sarcasm_detection: formData.selected_features.includes('sarcasm'),
        enable_iq_analysis: formData.selected_features.includes('iq'),
        enable_bot_detection: formData.selected_features.includes('bot'),
      };
      
      const result = await createAnalysis(payload);
      if (!result || !result.id) {
        setError('Failed to create analysis: No result ID returned');
        return;
      }
      
      setError('');
      navigate(`/analysis/${result.id}/processing`);
    } catch (err: unknown) {
      console.error('Error creating analysis:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to create analysis';
      setError(errorMessage);
    }
  };

  // Add a dedicated handler for the source select
  const handleSourceChange = (event: SelectChangeEvent<string[]>) => {
    const { value } = event.target;
    setFormData({
      ...formData,
      source: typeof value === 'string' ? value.split(',') : value,
    });
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Sentiment Analysis
        </Typography>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        <form onSubmit={handleSubmit} noValidate>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Search Query"
                name="query"
                value={formData.query}
                onChange={handleChange}
                margin="normal"
                required
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth margin="normal">
                <InputLabel id="source-label">Source</InputLabel>
                <Select
                  labelId="source-label"
                  name="source"
                  multiple
                  value={formData.source}
                  onChange={handleSourceChange}
                  label="Source"
                  renderValue={(selected) => selected.map(
                    (val) => SOURCES.find((s) => s.value === val)?.label || val
                  ).join(', ')}
                >
                  {SOURCES.map((source) => (
                    <MenuItem key={source.value} value={source.value}>
                      <Checkbox checked={formData.source.indexOf(source.value) > -1} />
                      <ListItemText primary={source.label} />
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <Box sx={{ mb: 3 }}>
                <FormControl fullWidth>
                  <Autocomplete
                    multiple
                    id="llm-select"
                    options={MODELS.map(model => model.value)}
                    value={formData.selected_llms}
                    onChange={(_, newValue) => {
                      setFormData(prev => ({
                        ...prev,
                        selected_llms: newValue
                      }));
                    }}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        label="Select LLM Models"
                        placeholder="Choose models"
                        required
                        error={!!error && error.toLowerCase().includes('model')}
                        helperText={error && error.toLowerCase().includes('model') ? error : ''}
                      />
                    )}
                    renderOption={(props, option) => {
                      // eslint-disable-next-line @typescript-eslint/no-unused-vars
                      const { key: keyProp, ...otherProps } = props;
                      return (
                        <li {...otherProps}>
                          {MODELS.find(m => m.value === option)?.label || option}
                        </li>
                      );
                    }}
                  />
                </FormControl>
              </Box>
            </Grid>
            <Grid item xs={12}>
              {formData.source.includes('reddit') && (
                <Box sx={{ mt: 2 }}>
                  <FormControl fullWidth margin="normal">
                    <Autocomplete
                      multiple
                      id="subreddits"
                      options={POPULAR_SUBREDDITS}
                      value={formData.subreddits}
                      onChange={handleSubredditChange}
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          label="Select Subreddits"
                          placeholder="Choose subreddits"
                        />
                      )}
                      renderOption={(props, option, { selected }) => {
                        // eslint-disable-next-line @typescript-eslint/no-unused-vars
                        const { key: keyProp, ...otherProps } = props;
                        return (
                          <li {...otherProps}>
                            <Checkbox
                              style={{ marginRight: 8 }}
                              checked={selected}
                            />
                            <ListItemText primary={option} />
                          </li>
                        );
                      }}
                    />
                  </FormControl>
                  <TextField
                    fullWidth
                    label="Add Custom Subreddit"
                    value={customSubreddit}
                    onChange={(e) => setCustomSubreddit(e.target.value)}
                    onKeyPress={handleCustomSubredditAdd}
                    helperText="Press Enter to add a custom subreddit"
                    sx={{ mt: 2 }}
                  />
                </Box>
              )}
            </Grid>
            <Grid item xs={12}>
              <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                <DatePicker
                  label="Start Date"
                  value={formData.start_date}
                  onChange={(newValue) => {
                    setFormData(prev => ({
                      ...prev,
                      start_date: newValue
                    }));
                  }}
                  renderInput={(params) => (
                    <TextField 
                      {...params} 
                      fullWidth 
                      required
                      error={!formData.start_date}
                      helperText={!formData.start_date ? 'Start date is required' : ''}
                    />
                  )}
                />
                <DatePicker
                  label="End Date"
                  value={formData.end_date}
                  onChange={(newValue) => {
                    setFormData(prev => ({
                      ...prev,
                      end_date: newValue
                    }));
                  }}
                  renderInput={(params) => (
                    <TextField 
                      {...params} 
                      fullWidth 
                      required
                      error={!formData.end_date}
                      helperText={!formData.end_date ? 'End date is required' : ''}
                    />
                  )}
                />
              </Box>
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth margin="normal">
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={formData.include_images}
                      onChange={(e) => setFormData({ ...formData, include_images: e.target.checked })}
                      name="include_images"
                    />
                  }
                  label="Include Image Analysis"
                />
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              {ANALYSIS_FEATURES.map((feature) => (
                <FormControl key={feature.value} fullWidth margin="normal">
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={formData.selected_features.includes(feature.value)}
                        onChange={(e) => {
                          const newValue = e.target.checked;
                          setFormData({
                            ...formData,
                            selected_features: newValue
                              ? [...formData.selected_features, feature.value]
                              : formData.selected_features.filter(f => f !== feature.value)
                          });
                        }}
                        name={feature.value}
                      />
                    }
                    label={`Enable ${feature.label}`}
                  />
                </FormControl>
              ))}
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                disabled={!formData.start_date || !formData.end_date}
              >
                Analyze
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Container>
  );
}

export default AnalysisForm; 