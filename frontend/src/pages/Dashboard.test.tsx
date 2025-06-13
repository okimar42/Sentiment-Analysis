import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Dashboard from './Dashboard.jsx';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import { NotificationProvider } from '../contexts/NotificationContext';

// Mock the analysis API module
vi.mock('../services/analysis.api', () => ({
  getAnalyses: vi.fn(),
}));

import { getAnalyses } from '../services/analysis.api';

const renderWithRouter = (ui) => {
  return render(<BrowserRouter>{ui}</BrowserRouter>);
};

describe('Dashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows loading spinner initially', () => {
    (getAnalyses as any).mockImplementation(() => new Promise(() => {})); // Never resolves
    renderWithRouter(<NotificationProvider><Dashboard /></NotificationProvider>);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('shows error state if API fails', async () => {
    (getAnalyses as any).mockRejectedValueOnce(new Error('Failed to fetch analyses'));
    renderWithRouter(<NotificationProvider><Dashboard /></NotificationProvider>);
    await waitFor(() => {
      expect(screen.getByText(/failed to fetch analyses/i)).toBeInTheDocument();
    });
  });

  it('renders analyses when API succeeds', async () => {
    (getAnalyses as any).mockResolvedValueOnce([
      { id: 1, query: 'test1', status: 'completed', source: ['twitter'] },
      { id: 2, query: 'test2', status: 'pending', source: ['reddit'] },
    ]);
    renderWithRouter(<NotificationProvider><Dashboard /></NotificationProvider>);
    expect(await screen.findByText('test1')).toBeInTheDocument();
    expect(screen.getByText('test2')).toBeInTheDocument();
  });

  it('navigates to new analysis on button click', async () => {
    (getAnalyses as any).mockResolvedValueOnce([]);
    renderWithRouter(<NotificationProvider><Dashboard /></NotificationProvider>);
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /new analysis/i })).toBeInTheDocument();
    });
    fireEvent.click(screen.getByRole('button', { name: /new analysis/i }));
    await waitFor(() => {
      expect(window.location.pathname).toMatch(/new-analysis/);
    });
  });
}); 