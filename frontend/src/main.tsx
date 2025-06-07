import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import React, { Component } from 'react'
import type { ReactNode } from 'react'

class ErrorBoundary extends Component<{ children: ReactNode }, { hasError: boolean; error: unknown }> {
  constructor(props: { children: ReactNode }) {
    super(props)
    this.state = { hasError: false, error: null }
  }
  static getDerivedStateFromError(error: unknown) {
    return { hasError: true, error }
  }
  componentDidCatch(error: unknown, info: unknown) {
    // Log error to console for diagnosis
    console.error('ErrorBoundary caught:', error, info)
  }
  render() {
    if (this.state.hasError) {
      let message = 'Unknown error';
      if (typeof this.state.error === 'string') message = this.state.error;
      else if (this.state.error instanceof Error) message = this.state.error.message;
      return (
        <div style={{ color: 'red', padding: 32 }}>
          <h1>Something went wrong.</h1>
          <pre>{message}</pre>
        </div>
      )
    }
    return this.props.children
  }
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
)
