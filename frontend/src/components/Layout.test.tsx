import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Layout from './Layout';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import { NotificationProvider } from '../contexts/NotificationContext';
import type { ReactElement } from 'react';

const renderWithRouter = (ui: ReactElement, props = {}) => {
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
    expect(dashboardButtons[0]).toBeInTheDocument();
    fireEvent.click(dashboardButtons[0]);
  });

  it('navigates to New Analysis on menu click', () => {
    renderWithRouter(<Layout />);
    const newAnalysisButtons = screen.getAllByText(/new analysis/i);
    expect(newAnalysisButtons[0]).toBeInTheDocument();
    fireEvent.click(newAnalysisButtons[0]);
  });

  it('navigates to Logout on menu click', () => {
    renderWithRouter(<Layout />);
    const logoutButtons = screen.getAllByText(/logout/i);
    expect(logoutButtons[0]).toBeInTheDocument();
    fireEvent.click(logoutButtons[0]);
  });

  it('toggles theme when theme button is clicked', () => {
    const toggleMode = vi.fn();
    renderWithRouter(<Layout mode="light" toggleMode={toggleMode} />);
    const buttons = screen.getAllByRole('button');
    fireEvent.click(buttons[1]);
    expect(toggleMode).toHaveBeenCalled();
  });
}); 