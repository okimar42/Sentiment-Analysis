import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { act, fireEvent, waitFor } from '@testing-library/react';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
// import AnalysisForm from './pages/AnalysisForm';
// import Login from './pages/Login';
// import * as reactRouterDom from 'react-router-dom';
// const mockNavigate = vi.fn();
// vi.mock('react-router-dom', async () => {
//   const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom');
//   return {
//     ...actual,
//     useNavigate: () => mockNavigate,
//   };
// });
// vi.mock('./services/api', () => ({
//   login: vi.fn().mockResolvedValue({ token: 'test-token' }),
//   getAnalyses: vi.fn().mockResolvedValue([
//     { id: '1', query: 'AAPL', source: 'reddit', model: 'vader', created_at: new Date().toISOString() }
//   ]),
//   getAnalysis: vi.fn().mockResolvedValue({ id: '123', query: 'AAPL', source: 'reddit', model: 'vader', created_at: new Date().toISOString() }),
//   getAnalysisSummary: vi.fn().mockResolvedValue({ summary: 'Test summary', sentiment: 0.5 }),
//   getAnalysisFullDetails: vi.fn().mockResolvedValue({ id: '123', summary: { summary: 'Test summary', sentiment: 0.5 }, results: [] }),
//   createAnalysis: vi.fn().mockResolvedValue({ id: '124', query: 'TSLA', source: 'twitter', model: 'vader', created_at: new Date().toISOString() }),
//   getSentimentByDate: vi.fn().mockResolvedValue([]),
//   getIQDistribution: vi.fn().mockResolvedValue([]),
//   getBotAnalysis: vi.fn().mockResolvedValue([]),
//   getGemmaStatus: vi.fn().mockResolvedValue({ status: 'ok' }),
//   getAnalysisResults: vi.fn().mockResolvedValue([]),
//   updateSentiment: vi.fn().mockResolvedValue({}),
//   searchAnalysisResults: vi.fn().mockResolvedValue([]),
//   // login: vi.fn().mockResolvedValue({ token: 'test-token' }),
//   // Add more mocks as needed for other API functions
// }));
import Login from './pages/Login';

describe('Direct Login render isolation', () => {
  it('renders Login directly (no App, no providers)', () => {
    render(<Login />);
// @jest-environment jsdom
import { vi } from 'vitest';
import '@testing-library/jest-dom';
import { render, screen, fireEvent, act } from '@testing-library/react';
import * as api from './services/api';
import App from './App';
import { NotificationProvider } from './contexts/NotificationContext';

// Mock getAnalyses to return a sample analysis for Dashboard
vi.spyOn(api, 'getAnalyses').mockImplementation(async () => [
  { id: '1', query: 'AAPL', source: 'reddit', model: 'vader', created_at: new Date().toISOString() }
]);

describe('App routing and theming', () => {
  it('renders Dashboard on /', async () => {
    window.history.pushState({}, '', '/');
    await act(async () => {
      render(<NotificationProvider><App /></NotificationProvider>);
    });
    expect(await screen.findByText(/Recent Analyses/i)).toBeInTheDocument();
    expect(await screen.findByText(/AAPL/i)).toBeInTheDocument();
  });

  it('renders Login on /login', () => {
    window.history.pushState({}, '', '/login');
    act(() => {
      render(<NotificationProvider><App /></NotificationProvider>);
    });
    expect(screen.getByRole('heading', { name: /Login/i })).toBeInTheDocument();
  });
});

// afterEach(() => {
//   vi.useRealTimers();
//   vi.clearAllMocks();
// });
// beforeEach(() => {
//   vi.useFakeTimers();
// }); 