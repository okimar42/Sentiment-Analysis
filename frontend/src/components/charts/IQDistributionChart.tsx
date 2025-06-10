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
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
} from 'recharts';

interface IQDistributionChartProps {
  data: Array<{
    iq: number;
    count: number;
  }>;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

export const IQDistributionChart: React.FC<IQDistributionChartProps> = ({ data }) => {
  const [chartType, setChartType] = React.useState<'bar' | 'pie'>('bar');

  return (
    <Paper style={{ padding: '20px' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6" gutterBottom sx={{ flexGrow: 1 }}>
          IQ Distribution
        </Typography>
        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>Graph</InputLabel>
          <Select
            value={chartType}
            label="Graph"
            onChange={(e) => setChartType(e.target.value as 'bar' | 'pie')}
          >
            <MenuItem value="bar">Bar</MenuItem>
            <MenuItem value="pie">Pie</MenuItem>
          </Select>
        </FormControl>
      </Box>
      {chartType === 'bar' ? (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
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
              data={data}
              dataKey="count"
              nameKey="iq"
              cx="50%"
              cy="50%"
              outerRadius={80}
              fill="#82ca9d"
              label={({ iq, percent }) => `IQ ${iq}: ${(percent * 100).toFixed(0)}%`}
            >
              {data.map((entry, index) => (
                <Cell key={`cell-iq-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      )}
    </Paper>
  );
};