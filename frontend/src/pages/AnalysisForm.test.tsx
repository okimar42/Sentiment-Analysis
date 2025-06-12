// Mock setup for Vitest hoisting
vi.mock('../services/analysis.api', () => ({
  createAnalysis: vi.fn(),
  getGemmaStatus: vi.fn(),
}));

// Mock useNavigate globally before any tests run
vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal();
  return { ...actual, useNavigate: () => vi.fn() };
});

import React from 'react';
import { render, screen, cleanup } from '@testing-library/react';
import '@testing-library/jest-dom';
import AnalysisForm from './AnalysisForm';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';

const renderWithRouter = (ui: React.ReactElement) => {
  return render(
    <BrowserRouter>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        {ui}
      </LocalizationProvider>
    </BrowserRouter>
  );
};

describe('AnalysisForm', () => {
  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
  });

  it('renders form fields', () => {
    renderWithRouter(<AnalysisForm />);
    expect(screen.getByLabelText(/search query/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/source/i)).toBeInTheDocument();
    // Just check that the form renders without errors
    expect(screen.getByText(/sentiment analysis/i)).toBeInTheDocument();
  });

  it('renders analyze button', () => {
    renderWithRouter(<AnalysisForm />);
    expect(screen.getByRole('button', { name: /analyze/i })).toBeInTheDocument();
  });
}); 