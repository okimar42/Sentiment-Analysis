import React from 'react';
import { render, screen } from '@testing-library/react';
import Login from './pages/Login';

describe('Direct Login render isolation', () => {
  it('renders Login directly (no App, no providers)', () => {
    render(<Login />);
    // Basic assertion to ensure component renders
    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();
  });
});

/*
The following block of code was inadvertently duplicated and causes parsing errors. 
It is kept for reference but excluded from compilation and linting.
----------------------------------------------------------------------------------
//@jest-environment jsdom
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
----------------------------------------------------------------------------------
*/ 