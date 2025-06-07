import React from 'react';
import {
  Paper,
  Grid,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox,
  Typography,
  Slider,
} from '@mui/material';

interface SearchFiltersProps {
  searchParams: {
    q: string;
    sentiment: string;
    sarcasm: boolean | null;
    bot: boolean | null;
    min_iq: number;
  };
  onSearchChange: (field: string, value: unknown) => void;
}

export const SearchFilters: React.FC<SearchFiltersProps> = ({
  searchParams,
  onSearchChange,
}) => {
  return (
    <Paper sx={{ p: 2, mb: 2 }}>
      <Grid container spacing={2}>
        {/* Search Input */}
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Search"
            value={searchParams.q}
            onChange={(e) => onSearchChange('q', e.target.value)}
            placeholder="Search by content..."
          />
        </Grid>

        {/* Sentiment Filter */}
        <Grid item xs={12} md={2}>
          <FormControl fullWidth>
            <InputLabel>Sentiment</InputLabel>
            <Select
              value={searchParams.sentiment}
              onChange={(e) => onSearchChange('sentiment', e.target.value)}
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
        <Grid item xs={12} md={2}>
          <FormControlLabel
            control={
              <Checkbox
                checked={searchParams.sarcasm === true}
                onChange={(e) => onSearchChange('sarcasm', e.target.checked)}
                indeterminate={searchParams.sarcasm === null}
              />
            }
            label="Sarcastic"
          />
        </Grid>

        {/* Bot Filter */}
        <Grid item xs={12} md={2}>
          <FormControlLabel
            control={
              <Checkbox
                checked={searchParams.bot === true}
                onChange={(e) => onSearchChange('bot', e.target.checked)}
                indeterminate={searchParams.bot === null}
              />
            }
            label="Bots"
          />
        </Grid>

        {/* IQ Filter */}
        <Grid item xs={12} md={2}>
          <FormControl fullWidth>
            <Typography gutterBottom>Min IQ: {searchParams.min_iq}</Typography>
            <Slider
              value={searchParams.min_iq}
              onChange={(e, newValue) => onSearchChange('min_iq', newValue)}
              min={0}
              max={1}
              step={0.1}
              valueLabelDisplay="auto"
            />
          </FormControl>
        </Grid>
      </Grid>
    </Paper>
  );
};