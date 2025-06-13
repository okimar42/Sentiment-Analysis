import { render } from '@testing-library/react';
import React from 'react';
import { SentimentOverTimeAreaChart } from './SentimentOverTimeAreaChart';
import type { AnalysisResult } from '../../services/types';

const sampleResults: AnalysisResult[] = [
  { id: '1', content: 'Good', score: 0.2, post_date: '2025-06-12T10:00:00Z', perceived_iq: 0.5, bot_probability: 0.1 },
  { id: '2', content: 'Bad', score: -0.3, post_date: '2025-06-12T11:00:00Z', perceived_iq: 0.4, bot_probability: 0.2 },
];

describe('SentimentOverTimeAreaChart', () => {
  it('renders without crashing', () => {
    render(<SentimentOverTimeAreaChart results={sampleResults} />);
  });
});