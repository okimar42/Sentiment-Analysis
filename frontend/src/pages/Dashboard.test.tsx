import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Dashboard from './Dashboard.jsx';
import { getAnalyses } from '../services/api';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';

vi.mock('../services/api');

const renderWithRouter = (ui) => {
  return render(<BrowserRouter>{ui}</BrowserRouter>);
};

describe('Dashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows loading spinner initially', () => {
    renderWithRouter(<Dashboard />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('shows error state if API fails', async () => {
    getAnalyses.mockRejectedValueOnce(new Error('Failed to fetch analyses'));
    renderWithRouter(<Dashboard />);
    await waitFor(() => {
      expect(screen.getByText(/failed to fetch analyses/i)).toBeInTheDocument();
    });
  });

  it('renders analyses when API succeeds', async () => {
    getAnalyses.mockResolvedValueOnce([
      { id: 1, query: 'test1', status: 'completed', source: ['twitter'] },
      { id: 2, query: 'test2', status: 'pending', source: ['reddit'] },
    ]);
    renderWithRouter(<Dashboard />);
    expect(await screen.findByText('test1')).toBeInTheDocument();
    expect(screen.getByText('test2')).toBeInTheDocument();
  });

  it('navigates to new analysis on button click', async () => {
    getAnalyses.mockResolvedValueOnce([]);
    renderWithRouter(<Dashboard />);
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /new analysis/i })).toBeInTheDocument();
    });
    fireEvent.click(screen.getByRole('button', { name: /new analysis/i }));
    await waitFor(() => {
      expect(window.location.pathname).toMatch(/new-analysis/);
    });
  });
}); 