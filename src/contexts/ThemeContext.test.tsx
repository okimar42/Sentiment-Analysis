import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { ThemeProvider, useTheme } from './ThemeContext';

describe('ThemeContext', () => {
  function TestComponent() {
    const { themeId, setTheme, availableThemes } = useTheme();
    return (
      <div>
        <span data-testid="theme-id">{themeId}</span>
        <button onClick={() => setTheme('dracula')}>Set Dracula</button>
        <span data-testid="theme-count">{availableThemes.length}</span>
      </div>
    );
  }

  beforeEach(() => {
    localStorage.clear();
  });

  it('provides the default theme', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );
    expect(screen.getByTestId('theme-id').textContent).toBe('gruvbox-dark');
  });

  it('switches theme and persists it', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );
    fireEvent.click(screen.getByText('Set Dracula'));
    expect(screen.getByTestId('theme-id').textContent).toBe('dracula');
    // Should persist to localStorage
    expect(localStorage.getItem('themeId')).toBe('dracula');
  });

  it('loads theme from localStorage', () => {
    localStorage.setItem('themeId', 'monokai');
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );
    expect(screen.getByTestId('theme-id').textContent).toBe('monokai');
  });

  it('provides all available themes', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );
    expect(Number(screen.getByTestId('theme-count').textContent)).toBeGreaterThan(5);
  });
}); 