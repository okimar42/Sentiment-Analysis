import React from 'react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from 'recharts';
import type { AnalysisResult } from '../../services/types';

interface SentimentOverTimeAreaChartProps {
  results: AnalysisResult[];
}

// Helper to aggregate sentiment counts per date (YYYY-MM-DD)
const buildChartData = (results: AnalysisResult[]) => {
  const dateMap: Record<string, { positive: number; neutral: number; negative: number }> = {};
  results.forEach((r) => {
    if (!r.post_date) return;
    const dateStr = new Date(r.post_date).toISOString().split('T')[0];
    if (!dateMap[dateStr]) {
      dateMap[dateStr] = { positive: 0, neutral: 0, negative: 0 };
    }
    // Determine sentiment bucket using same thresholds as backend search
    const score = r.score ?? 0;
    if (score > 0.05) {
      dateMap[dateStr].positive += 1;
    } else if (score < -0.05) {
      dateMap[dateStr].negative += 1;
    } else {
      dateMap[dateStr].neutral += 1;
    }
  });
  return Object.entries(dateMap)
    .sort(([a], [b]) => (a > b ? 1 : -1))
    .map(([date, counts]) => ({ date, ...counts }));
};

export const SentimentOverTimeAreaChart: React.FC<SentimentOverTimeAreaChartProps> = ({ results }) => {
  const data = React.useMemo(() => buildChartData(results), [results]);

  if (data.length === 0) return null;

  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis allowDecimals={false} />
        <Tooltip />
        <Legend />
        <Area type="monotone" dataKey="positive" stackId="1" stroke="#00C49F" fill="#00C49F" />
        <Area type="monotone" dataKey="neutral" stackId="1" stroke="#FFBB28" fill="#FFBB28" />
        <Area type="monotone" dataKey="negative" stackId="1" stroke="#FF8042" fill="#FF8042" />
      </AreaChart>
    </ResponsiveContainer>
  );
};

export default SentimentOverTimeAreaChart;