import { render, screen } from '@testing-library/react';
import React from 'react';

describe('Minimal Login', () => {
  function Login() {
    return <h1>Login</h1>;
  }
  it('renders heading', () => {
    render(<Login />);
    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();
  });
}); 