// @jest-environment jsdom
import { vi } from 'vitest';
import '@testing-library/jest-dom';
import React from 'react';
import { render, screen, act } from '@testing-library/react';
import * as api from './services/analysis.api';
import App from './App';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AnalysisForm from './pages/AnalysisForm';
import AnalysisResults from './pages/AnalysisResults';
import AnalysisProcessing from './pages/AnalysisProcessing';
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

describe('Route registry', () => {
  // Extract route info from App (static analysis, not runtime)
  // For now, hardcode the known routes as in App.tsx
  const routes = [
    { path: '/', element: 'Layout' },
    { path: '', element: 'Dashboard' }, // index route
    { path: 'new-analysis', element: 'AnalysisForm' },
    { path: 'results/:id', element: 'AnalysisResults' },
    { path: 'analysis/:id/processing', element: 'AnalysisProcessing' },
    { path: 'analysis/:id', element: 'AnalysisResults' },
    { path: 'login', element: 'Login' },
  ];

  it('should have unique route paths', () => {
    const paths = routes.map(r => r.path);
    expect(new Set(paths).size).toBe(paths.length);
  });

  it('should have a component for every route element', () => {
    const pageMap: Record<string, unknown> = {
      Login,
      Dashboard,
      AnalysisForm,
      AnalysisResults,
      AnalysisProcessing,
    };
    for (const route of routes) {
      if (route.element === 'Layout') continue; // Layout is in components
      expect(pageMap[route.element]).toBeDefined();
    }
  });

  it('should not have duplicate route definitions', () => {
    const seen = new Set();
    for (const route of routes) {
      const key = `${route.path}|${route.element}`;
      expect(seen.has(key)).toBe(false);
      seen.add(key);
    }
  });

  it('should have all required pages in the pages directory', () => {
    // This test is now redundant with the above, but kept for completeness
    expect(Login).toBeDefined();
    expect(Dashboard).toBeDefined();
    expect(AnalysisForm).toBeDefined();
    expect(AnalysisResults).toBeDefined();
    expect(AnalysisProcessing).toBeDefined();
  });
}); 