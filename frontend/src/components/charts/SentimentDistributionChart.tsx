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
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
} from 'recharts';
import type { AnalysisSummary } from '../../services/api';

interface SentimentDistributionChartProps {
  summary: AnalysisSummary;
}

const COLORS = ['#4CAF50', '#FFC107', '#F44336'];

export const SentimentDistributionChart: React.FC<SentimentDistributionChartProps> = ({ summary }) => {
  const [chartType, setChartType] = React.useState<'pie' | 'bar'>('pie');

  const sentimentData = [
    { name: 'Positive', value: summary.sentiment_distribution.positive },
    { name: 'Neutral', value: summary.sentiment_distribution.neutral },
    { name: 'Negative', value: summary.sentiment_distribution.negative },
  ];

  return (
    <Paper style={{ padding: '20px' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6" gutterBottom sx={{ flexGrow: 1 }}>
          Sentiment Distribution
        </Typography>
        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>Graph</InputLabel>
          <Select
            value={chartType}
            label="Graph"
            onChange={(e) => setChartType(e.target.value as 'pie' | 'bar')}
          >
            <MenuItem value="pie">Pie</MenuItem>
            <MenuItem value="bar">Bar</MenuItem>
          </Select>
        </FormControl>
      </Box>
      {chartType === 'pie' ? (
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
  );
};