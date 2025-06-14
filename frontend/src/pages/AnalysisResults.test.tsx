import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import AnalysisResults from './AnalysisResults';
import { vi } from 'vitest';
import * as api from '../services/analysis.api';
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

vi.mock('../services/analysis.api', () => {
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
      id: '1',
      query: 'test',
      source: ['twitter'],
      model: 'gpt-4',
      created_at: '2024-01-01T00:00:00Z',
      status: 'completed',
      twitter_grok_summary: 'Grok says: bullish!',
      results: [
        { id: '1', content: 'test tweet', score: 0.2, perceived_iq: 0.5, bot_probability: 0.1, post_date: new Date().toISOString(), source_type: 'twitter' }
      ],
      summary: { total_posts: 1, average_score: 0.5, sentiment_distribution: { positive: 1, negative: 0, neutral: 0 }, sentiment_percentages: { positive: 100, negative: 0, neutral: 0 } },
    });
  });

  it('renders loading spinner and then main content', async () => {
    render(<NotificationProvider><AnalysisResults /></NotificationProvider>);
    // Spinner should be present initially
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
    // Wait for the main heading to appear
    expect(await screen.findByText(/analysis results/i)).toBeInTheDocument();
  });

  it('renders error state', async () => {
    getAnalysisFullDetails.mockRejectedValueOnce(new Error('Test error'));
    render(<NotificationProvider><AnalysisResults /></NotificationProvider>);
    expect(await screen.findByText(/error: test error/i)).toBeInTheDocument();
  });

  it('renders no data state', async () => {
    getAnalysisFullDetails.mockResolvedValueOnce({
      id: '',
      query: '',
      source: '',
      model: '',
      created_at: '',
      status: '',
      twitter_grok_summary: '',
      results: [],
      summary: {
        total_posts: 0,
        average_score: 0,
        sentiment_distribution: { positive: 0, negative: 0, neutral: 0 },
        sentiment_percentages: { positive: 0, negative: 0, neutral: 0 },
      },
    });
    render(<NotificationProvider><AnalysisResults /></NotificationProvider>);
    // Should show debug info (spinner and debug text)
    expect(await screen.findByText(/debug: status/i)).toBeInTheDocument();
    expect(screen.getByText(/debug: full/i)).toBeInTheDocument();
  });

  it('renders summary and Twitter Grok summary', async () => {
    render(<NotificationProvider><AnalysisResults /></NotificationProvider>);
    // There are two headings: 'Summary' and 'Twitter Grok Summary'
    const summaryHeadings = await screen.findAllByText(/summary/i);
    expect(summaryHeadings.length).toBeGreaterThan(1);
    expect(screen.getByText(/grok says: bullish!/i)).toBeInTheDocument();
  });

  it('toggles sentiment chart type', async () => {
    render(<NotificationProvider><AnalysisResults /></NotificationProvider>);
    // There are two 'Sentiment Distribution' elements: heading and summary text
    const sentimentHeadings = await screen.findAllByText(/sentiment distribution/i);
    expect(sentimentHeadings.length).toBeGreaterThan(0);
    // Pie chart is default
    expect(screen.getByText(/pie chart/i)).toBeInTheDocument();
    // Switch to bar chart
    const graphSelect = screen.getByRole('combobox', { name: /graph/i });
    graphSelect.focus();
    // Open the dropdown (simulate arrow down or mouse click)
    // fireEvent.mouseDown(graphSelect); // alternative
    graphSelect.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowDown', bubbles: true }));
    // Click the 'Bar Chart' option
    const barOption = await screen.findByRole('option', { name: /bar chart/i });
    barOption.click();
    expect(screen.getByText(/bar chart/i)).toBeInTheDocument();
  });

  it('renders search and filter UI', async () => {
    render(<NotificationProvider><AnalysisResults /></NotificationProvider>);
    expect(await screen.findByLabelText(/search/i)).toBeInTheDocument();
    // Sentiment is a select, use getAllByLabelText
    expect(screen.getAllByLabelText(/sentiment/i).length).toBeGreaterThan(0);
    expect(screen.getAllByLabelText(/sarcastic/i).length).toBeGreaterThan(0);
    expect(screen.getAllByLabelText(/bot/i).length).toBeGreaterThan(0);
  });
});

// ... (rest of the test code as in AnalysisResults.test.js) ... 