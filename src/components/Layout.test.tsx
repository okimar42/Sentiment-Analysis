import React from 'react';
import { render, screen, fireEvent, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { ThemeProvider } from '../contexts/ThemeContext';
import Layout from './Layout';

describe('Layout theme selection', () => {
  function renderLayout() {
    return render(
      <ThemeProvider>
        <MemoryRouter>
          <Layout />
        </MemoryRouter>
      </ThemeProvider>
    );
  }

  beforeEach(() => {
    localStorage.clear();
  });

  it('shows the current theme name in the palette button', () => {
    renderLayout();
    expect(screen.getByRole('button', { name: /gruvbox dark/i })).toBeInTheDocument();
  });

  it('opens the theme menu and lists themes', () => {
    renderLayout();
    fireEvent.click(screen.getByRole('button', { name: /gruvbox dark/i }));
    expect(screen.getByText(/dark themes/i)).toBeInTheDocument();
    expect(screen.getByText(/light themes/i)).toBeInTheDocument();
    expect(screen.getByText(/Dracula/)).toBeInTheDocument();
    expect(screen.getByText(/Gruvbox Light/)).toBeInTheDocument();
  });

  it('selects a new theme and persists it', () => {
    renderLayout();
    fireEvent.click(screen.getByRole('button', { name: /gruvbox dark/i }));
    fireEvent.click(screen.getByText('Dracula'));
    expect(screen.getByRole('button', { name: /dracula/i })).toBeInTheDocument();
    expect(localStorage.getItem('themeId')).toBe('dracula');
  });

  it('shows a checkmark next to the selected theme', () => {
    renderLayout();
    fireEvent.click(screen.getByRole('button', { name: /gruvbox dark/i }));
    const draculaItem = screen.getByText('Dracula').closest('li');
    fireEvent.click(draculaItem!);
    fireEvent.click(screen.getByRole('button', { name: /dracula/i }));
    const draculaMenuItem = screen.getByText('Dracula').closest('li');
    expect(within(draculaMenuItem!).getByTestId('CheckIcon')).toBeInTheDocument();
  });
}); 