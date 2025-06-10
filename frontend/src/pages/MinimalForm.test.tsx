import { render, screen } from '@testing-library/react';
import React from 'react';

describe('Minimal test', () => {
  it('renders hello', () => {
    render(<div>Hello</div>);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
}); 