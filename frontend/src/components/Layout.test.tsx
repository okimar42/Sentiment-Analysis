import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Layout from './Layout.jsx';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import { NotificationProvider } from '../contexts/NotificationContext';

const renderWithRouter = (ui, props = {}) => {
  return render(
    <BrowserRouter>
      <NotificationProvider>
        {React.cloneElement(ui, props)}
      </NotificationProvider>
    </BrowserRouter>
  );
};

describe('Layout', () => {
  it('renders children', () => {
    renderWithRouter(<Layout><div>Child Content</div></Layout>);
    expect(screen.getByText('Child Content')).toBeInTheDocument();
  });

  it('navigates to Dashboard on menu click', () => {
    renderWithRouter(<Layout />);
    const dashboardButtons = screen.getAllByText(/dashboard/i);
    fireEvent.click(dashboardButtons[0]);
    expect(window.location.pathname).toBe('/');
  });

  it('navigates to New Analysis on menu click', () => {
    renderWithRouter(<Layout />);
    const newAnalysisButtons = screen.getAllByText(/new analysis/i);
    fireEvent.click(newAnalysisButtons[0]);
    expect(window.location.pathname).toBe('/new-analysis');
  });

  it('navigates to Logout on menu click', () => {
    renderWithRouter(<Layout />);
    const logoutButtons = screen.getAllByText(/logout/i);
    fireEvent.click(logoutButtons[0]);
    expect(window.location.pathname).toBe('/login');
  });

  it('toggles theme when theme button is clicked', () => {
    const toggleMode = vi.fn();
    renderWithRouter(<Layout mode="light" toggleMode={toggleMode} />);
    const buttons = screen.getAllByRole('button');
    fireEvent.click(buttons[1]);
    expect(toggleMode).toHaveBeenCalled();
  });
}); 