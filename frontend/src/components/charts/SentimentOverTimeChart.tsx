import React from 'react';
import {
  Paper,
  Box,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface SentimentOverTimeChartProps {
  data: Array<{
    date: string;
    score: number;
    count: number;
  }>;
}

export const SentimentOverTimeChart: React.FC<SentimentOverTimeChartProps> = ({ data }) => {
  const [chartType, setChartType] = React.useState<'line' | 'bar'>('line');

  return (
    <Paper style={{ padding: '20px' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6" gutterBottom sx={{ flexGrow: 1 }}>
          Sentiment Over Time
        </Typography>
        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>Graph</InputLabel>
          <Select
            value={chartType}
            label="Graph"
            onChange={(e) => setChartType(e.target.value as 'line' | 'bar')}
          >
            <MenuItem value="line">Line</MenuItem>
            <MenuItem value="bar">Bar</MenuItem>
          </Select>
        </FormControl>
      </Box>
      {chartType === 'line' ? (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
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
          <BarChart data={data}>
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
  );
};