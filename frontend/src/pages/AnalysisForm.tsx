import React, { useState } from 'react';
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
  Chip,
  Alert,
  Autocomplete,
  Checkbox,
  ListItemText,
  FormControlLabel,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { createAnalysis } from '../services/api';
import type { SelectChangeEvent } from '@mui/material/Select';

const SOURCES = [
  { value: 'reddit', label: 'Reddit' },
  { value: 'twitter', label: 'Twitter' },
];

const MODELS = [
  { value: 'vader', label: 'VADER' },
  { value: 'gpt4', label: 'GPT-4' },
  { value: 'claude', label: 'Claude' },
  { value: 'gemini', label: 'Gemini' },
  { value: 'gemma', label: 'Gemma' },
  { value: 'grok', label: 'Grok' },
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

type FormData = {
  query: string;
  source: string[];
  model: string;
  subreddits: string[];
  start_date: Date;
  end_date: Date;
  include_images: boolean;
  selected_llms: string[];
  selected_features: string[];
};

function AnalysisForm() {
  const [formData, setFormData] = useState<FormData>({
    query: '',
    source: ['reddit'],
    model: 'vader',
    subreddits: POPULAR_SUBREDDITS,
    start_date: yesterday,
    end_date: today,
    include_images: true,
    selected_llms: ['vader'], // Initialize with default model
    selected_features: ['sarcasm', 'iq', 'bot'],
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

  const handleDateChange = (field: string) => (date: Date | null) => {
    if (date) {
      setFormData({
        ...formData,
        [field]: date,
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
    
    // Use fallback to formData.model if selected_llms is empty, with hardcoded fallback
    let selectedModels = formData.selected_llms.length > 0 ? formData.selected_llms : [formData.model];
    
    // Temporary hardcoded fallback for debugging
    if (selectedModels.length === 0 || !selectedModels[0]) {
      selectedModels = ['vader'];
    }
    
    try {
      const payload = {
        query: formData.query,
        source: formData.source,
        model: selectedModels[0].toLowerCase(), // Convert to lowercase
        subreddits: formData.subreddits,
        start_date: formData.start_date.toISOString(),
        end_date: formData.end_date.toISOString(),
        include_images: formData.include_images,
        selected_llms: selectedModels.map(model => model.toLowerCase()), // Convert all to lowercase
        enable_sarcasm_detection: formData.selected_features.includes('sarcasm'),
        enable_iq_analysis: formData.selected_features.includes('iq'),
        enable_bot_detection: formData.selected_features.includes('bot'),
      };
      
      console.log('Submitting payload:', payload);
      const result = await createAnalysis(payload);
      console.log('Analysis created successfully:', result);
      
      // Simple success message instead of complex reset/navigation
      setError('');
      alert(`Analysis created successfully! ID: ${result.id}`);
      
    } catch (err) {
      console.error('Error creating analysis:', err);
      setError('Failed to create analysis');
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
    <Container maxWidth="md">
      <Box sx={{ mt: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center">
            New Sentiment Analysis
          </Typography>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Search Query"
              name="query"
              value={formData.query}
              onChange={handleChange}
              margin="normal"
              required
            />
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
            <FormControl fullWidth margin="normal">
              <InputLabel id="model-label">Model</InputLabel>
              <Select
                labelId="model-label"
                multiple
                value={formData.selected_llms}
                onChange={(e) => setFormData({ ...formData, selected_llms: Array.isArray(e.target.value) ? e.target.value as string[] : [] })}
                renderValue={(selected) => (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip 
                        key={value} 
                        label={
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            {MODELS.find(m => m.value === value)?.label}
                          </Box>
                        }
                      />
                    ))}
                  </Box>
                )}
                label="Model"
              >
                {MODELS.map((model) => (
                  <MenuItem key={model.value} value={model.value}>
                    <Checkbox checked={formData.selected_llms.indexOf(model.value) > -1} />
                    <ListItemText 
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          {model.label}
                        </Box>
                      }
                    />
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
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
                    renderOption={(props, option, { selected }) => (
                      <li {...props}>
                        <Checkbox
                          style={{ marginRight: 8 }}
                          checked={selected}
                        />
                        <ListItemText primary={option} />
                      </li>
                    )}
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
            <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
              <DatePicker
                label="Start Date"
                value={formData.start_date}
                onChange={handleDateChange('start_date')}
                slotProps={{ textField: { fullWidth: true } }}
              />
              <DatePicker
                label="End Date"
                value={formData.end_date}
                onChange={handleDateChange('end_date')}
                slotProps={{ textField: { fullWidth: true } }}
              />
            </Box>
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
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              sx={{ mt: 3 }}
            >
              Start Analysis
            </Button>
          </form>
        </Paper>
      </Box>
    </Container>
  );
}

export default AnalysisForm; 