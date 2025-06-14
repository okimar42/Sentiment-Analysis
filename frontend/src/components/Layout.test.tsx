import React from 'react';
import { render, screen, fireEvent, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import Layout from './Layout';
import { BrowserRouter } from 'react-router-dom';
import { NotificationProvider } from '../contexts/NotificationContext';
import { ThemeProvider } from '../contexts/ThemeContext';
import type { ReactElement } from 'react';

const renderWithProviders = (ui: ReactElement, props = {}) => {
  return render(
    <ThemeProvider>
      <NotificationProvider>
        <BrowserRouter>
        {React.cloneElement(ui, props)}
        </BrowserRouter>
      </NotificationProvider>
    </ThemeProvider>
  );
};

describe('Layout theme selection', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('shows the current theme name in the palette button', () => {
    renderWithProviders(<Layout><div>Child Content</div></Layout>);
    expect(screen.getByRole('button', { name: /gruvbox dark/i })).toBeInTheDocument();
  });

  it('opens the theme menu and lists grouped themes', () => {
    renderWithProviders(<Layout />);
    fireEvent.click(screen.getByRole('button', { name: /gruvbox dark/i }));
    expect(screen.getByText(/dark themes/i)).toBeInTheDocument();
    expect(screen.getByText(/light themes/i)).toBeInTheDocument();
    expect(screen.getByText(/Dracula/)).toBeInTheDocument();
    expect(screen.getByText(/Gruvbox Light/)).toBeInTheDocument();
  });

  it('selects a new theme and persists it', () => {
    renderWithProviders(<Layout />);
    fireEvent.click(screen.getByRole('button', { name: /gruvbox dark/i }));
    fireEvent.click(screen.getByText('Dracula'));
    expect(screen.getByRole('button', { name: /dracula/i })).toBeInTheDocument();
    expect(localStorage.getItem('themeId')).toBe('dracula');
  });

  it('shows a checkmark next to the selected theme', () => {
    renderWithProviders(<Layout />);
    fireEvent.click(screen.getByRole('button', { name: /gruvbox dark/i }));
    const draculaMenuItems = screen.getAllByText('Dracula').map(el => el.closest('li')).filter(Boolean);
    fireEvent.click(draculaMenuItems[0]!);
    fireEvent.click(screen.getByRole('button', { name: /dracula/i }));
    const draculaMenuItem = draculaMenuItems[0];
    expect(within(draculaMenuItem!).getByTestId('CheckIcon')).toBeInTheDocument();
  });

  it('renders children', () => {
    renderWithProviders(<Layout><div>Child Content</div></Layout>);
    expect(screen.getByText('Child Content')).toBeInTheDocument();
  });

  it('navigates to Dashboard on menu click', () => {
    renderWithProviders(<Layout />);
    const dashboardButtons = screen.getAllByText(/dashboard/i);
    expect(dashboardButtons[0]).toBeInTheDocument();
    fireEvent.click(dashboardButtons[0]);
  });

  it('navigates to New Analysis on menu click', () => {
    renderWithProviders(<Layout />);
    const newAnalysisButtons = screen.getAllByText(/new analysis/i);
    expect(newAnalysisButtons[0]).toBeInTheDocument();
    fireEvent.click(newAnalysisButtons[0]);
  });

  it('navigates to Logout on menu click', () => {
    renderWithProviders(<Layout />);
    const logoutButtons = screen.getAllByText(/logout/i);
    expect(logoutButtons[0]).toBeInTheDocument();
    fireEvent.click(logoutButtons[0]);
  });
}); 