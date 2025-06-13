// @jest-environment jsdom
import { vi } from 'vitest';
import '@testing-library/jest-dom';
import React from 'react';
import { render, screen, act } from '@testing-library/react';
import * as api from './services/analysis.api';
import App from './App';
import Login from './pages/Login';
import { NotificationProvider } from './contexts/NotificationContext';

// Mock getAnalyses to return a sample analysis for Dashboard
vi.spyOn(api, 'getAnalyses').mockImplementation(async () => [
  { id: '1', query: 'AAPL', source: 'reddit', model: 'vader', created_at: new Date().toISOString() }
]);

describe('Direct Login render isolation', () => {
  it('renders Login directly (no App, no providers)', () => {
    render(<Login />);
    expect(screen.getByRole('heading', { name: /Login/i })).toBeInTheDocument();
  });
});

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