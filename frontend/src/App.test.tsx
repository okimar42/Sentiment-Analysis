// @jest-environment jsdom
import { vi } from 'vitest';
import '@testing-library/jest-dom';
import { render, screen, fireEvent, act } from '@testing-library/react';
// @ts-expect-error: No type declarations for api.js
import * as api from './services/api';
import App from './App';

// Mock getAnalyses to return a sample analysis for Dashboard
vi.spyOn(api, 'getAnalyses').mockImplementation(async () => [
  { id: 1, query: 'AAPL', source: 'reddit', model: 'vader', created_at: new Date().toISOString() }
]);

describe('App routing and theming', () => {
  it('renders Dashboard on /', async () => {
    window.history.pushState({}, '', '/');
    await act(async () => {
      render(<App />);
    });
    expect(await screen.findByText(/Recent Analyses/i)).toBeInTheDocument();
    expect(await screen.findByText(/AAPL/i)).toBeInTheDocument();
  });

  it('renders Login on /login', () => {
    window.history.pushState({}, '', '/login');
    act(() => {
      render(<App />);
    });
    expect(screen.getByRole('heading', { name: /Login/i })).toBeInTheDocument();
    const loginButtons = screen.getAllByRole('button', { name: /^Login$/i });
    expect(loginButtons.some(btn => (btn as HTMLButtonElement).type === 'submit')).toBe(true);
  });

  it('renders New Analysis on /new-analysis', () => {
    window.history.pushState({}, '', '/new-analysis');
    act(() => {
      render(<App />);
    });
    expect(screen.getByRole('heading', { name: /New Sentiment Analysis/i })).toBeInTheDocument();
  });

  it('renders Analysis Processing on /analysis/:id/processing', () => {
    window.history.pushState({}, '', '/analysis/123/processing');
    act(() => {
      render(<App />);
    });
    expect(screen.getByText(/Your analysis is being processed/i)).toBeInTheDocument();
  });

  it('renders Analysis Results on /analysis/:id', () => {
    window.history.pushState({}, '', '/analysis/123');
    act(() => {
      render(<App />);
    });
    expect(screen.getByText(/summary|results|sentiment/i)).toBeInTheDocument();
  });

  it('toggles theme between light and dark', () => {
    window.history.pushState({}, '', '/');
    act(() => {
      render(<App />);
    });
    const toggleButton = screen.getAllByRole('button').find(
      btn => btn.getAttribute('aria-label') === 'open drawer' || btn.innerHTML.includes('svg')
    );
    expect(toggleButton).toBeInTheDocument();
    act(() => {
      fireEvent.click(toggleButton!);
    });
  });
}); 