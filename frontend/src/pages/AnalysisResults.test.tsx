import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import AnalysisResults from './AnalysisResults';
import { vi } from 'vitest';
import * as api from '../services/api';
import { NotificationProvider } from '../contexts/NotificationContext';

// Mock ResizeObserver for recharts and MUI
beforeAll(() => {
  global.ResizeObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
  };
});

vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...(actual as Record<string, unknown>),
    useParams: () => ({ id: '1' }),
  };
});

vi.mock('../services/api', () => {
  const baseData = {
    analysis: { query: 'test', status: 'completed', source: ['twitter'], twitter_grok_summary: 'Grok says: bullish!' },
    summary: { total_posts: 1, average_score: 0.5, sentiment_distribution: { positive: 1, negative: 0, neutral: 0 }, sentiment_percentages: { positive: 100, negative: 0, neutral: 0 } },
    sentiment_by_date: [],
    iq_distribution: [],
    bot_analysis: {},
    results: [
      { id: '1', content: 'test tweet', score: 0.2, perceived_iq: 0.5, bot_probability: 0.1, post_date: new Date().toISOString(), source_type: 'twitter' }
    ],
  };
  return {
    getAnalysisFullDetails: vi.fn(() => Promise.resolve(baseData)),
    searchAnalysisResults: vi.fn(() => Promise.resolve({
      results: [
        { id: '1', content: 'test tweet', score: 0.2, perceived_iq: 0.5, bot_probability: 0.1, post_date: new Date().toISOString(), source_type: 'twitter' }
      ],
      total_count: 1,
      page: 1,
      page_size: 20,
      total_pages: 1,
    })),
    updateSentiment: vi.fn(() => {
      const result = {
        id: '1',
        content: 'test tweet',
        score: 0.5, // 50 after *100
        perceived_iq: 0.5,
        bot_probability: 0.1,
        post_date: new Date().toISOString(),
        source_type: 'twitter',
      };
      console.log('Mock updateSentiment returning:', result);
      return Promise.resolve(result);
    }),
  };
});

const getAnalysisFullDetails = vi.mocked(api.getAnalysisFullDetails);

describe('AnalysisResults', () => {
  beforeEach(() => {
    getAnalysisFullDetails.mockResolvedValue({
      analysis: { query: 'test', status: 'completed', source: ['twitter'], twitter_grok_summary: 'Grok says: bullish!' },
      summary: { total_posts: 1, average_score: 0.5, sentiment_distribution: { positive: 1, negative: 0, neutral: 0 }, sentiment_percentages: { positive: 100, negative: 0, neutral: 0 } },
      sentiment_by_date: [],
      iq_distribution: [],
      bot_analysis: {},
      results: [
        { id: '1', content: 'test tweet', score: 0.2, perceived_iq: 0.5, bot_probability: 0.1, post_date: new Date().toISOString(), source_type: 'twitter' }
      ],
    });
  });

  it('renders loading spinner and then main content', async () => {
    render(<NotificationProvider><AnalysisResults /></NotificationProvider>);
    // Spinner should be present initially
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
    // Wait for the main heading to appear
    expect(await screen.findByText(/analysis results/i)).toBeInTheDocument();
  });
});

// ... (rest of the test code as in AnalysisResults.test.js) ... 