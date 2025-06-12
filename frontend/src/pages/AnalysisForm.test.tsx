import React from 'react';
import { render, screen, fireEvent, waitFor, cleanup } from '@testing-library/react';
import '@testing-library/jest-dom';
import AnalysisForm from './AnalysisForm';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';

// Define mockNavigate at the module level
const mockNavigate = vi.fn();

// Mock useNavigate globally before any tests run
vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal();
  return { ...actual, useNavigate: () => mockNavigate };
});

// Shared mock functions
const createAnalysisMock = vi.fn();
const getGemmaStatusMock = vi.fn();

vi.mock('../services/api', async () => {
  const actual = await vi.importActual<typeof import('../services/api')>('../services/api');
  return {
    ...actual,
    createAnalysis: createAnalysisMock,
    getGemmaStatus: getGemmaStatusMock,
  };
});

vi.mock('../services/analysis.api', async () => {
  const actual = await vi.importActual<typeof import('../services/analysis.api')>('../services/analysis.api');
  return {
    ...actual,
    createAnalysis: createAnalysisMock,
    getGemmaStatus: getGemmaStatusMock,
  };
});

const renderWithRouter = (ui: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {ui}
    </BrowserRouter>
  );
};

describe('AnalysisForm', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    getGemmaStatusMock.mockResolvedValue({ status: 'ready' });
  });

  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
    vi.clearAllTimers();
    vi.useRealTimers();
  });

  beforeAll(() => {
    // Provide a minimal, typed mock for IntersectionObserver used by MUI components
    class MockIntersectionObserver implements IntersectionObserver {
      readonly root: Element | null = null;
      readonly rootMargin = '';
      readonly thresholds: ReadonlyArray<number> = [];
      disconnect(): void {/* noop */}
      observe(): void {/* noop */}
      takeRecords(): IntersectionObserverEntry[] { return []; }
      unobserve(): void {/* noop */}
    }
    (window as unknown as { IntersectionObserver: typeof MockIntersectionObserver }).IntersectionObserver = MockIntersectionObserver;
  });

  // Existing ResizeObserver mock
  global.ResizeObserver = class {
    observe() {/* noop */}
    unobserve() {/* noop */}
    disconnect() {/* noop */}
  };

  it('renders form fields', () => {
    renderWithRouter(<AnalysisForm />);
    expect(screen.getByLabelText(/query/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/source/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/model/i)).toBeInTheDocument();
  });

  // it('shows validation error if no model selected', async () => {
  //   renderWithRouter(<AnalysisForm />);
  //   fireEvent.change(screen.getByLabelText(/query/i), { target: { value: 'test' } });
  //   // Open the model Autocomplete dropdown
  //   const modelInput = screen.getByLabelText(/model/i);
  //   if (modelInput instanceof HTMLElement) {
  //     fireEvent.mouseDown(modelInput);
  //   }
  //   // Deselect the selected option (VADER)
  //   const vaderOptions = screen.getAllByText(/VADER/i);
  //   const vaderOption = vaderOptions.find(el => el.getAttribute && el.getAttribute('role') === 'option');
  //   if (vaderOption) {
  //     fireEvent.click(vaderOption); // This should deselect VADER
  //   } else {
  //     fireEvent.click(vaderOptions[0]);
  //   }
  //   // Close the dropdown
  //   if (document.activeElement instanceof HTMLElement) {
  //     fireEvent.keyDown(document.activeElement, { key: 'Escape', code: 'Escape' });
  //   }
  //   fireEvent.click(screen.getByRole('button', { name: /analyze/i }));
  //   const errorMessages = await screen.findAllByText(/please select at least one model/i);
  //   expect(errorMessages.length).toBeGreaterThan(0);
  // });

  it('shows error if backend fails', async () => {
    createAnalysisMock.mockRejectedValueOnce(new Error('Backend error'));
    renderWithRouter(<AnalysisForm />);
    fireEvent.change(screen.getByLabelText(/query/i), { target: { value: 'test' } });
    // Select a model
    fireEvent.mouseDown(screen.getByLabelText(/model/i));
    fireEvent.click(screen.getByRole('option', { name: /gpt-4/i }));
    fireEvent.keyDown(document.activeElement, { key: 'Escape', code: 'Escape' });
    fireEvent.click(screen.getByRole('button', { name: /analyze/i }));
    expect(await screen.findByText(/backend error/i)).toBeInTheDocument();
  });

  it('navigates on successful submission', async () => {
    createAnalysisMock.mockResolvedValueOnce({ id: 123 });
    renderWithRouter(<AnalysisForm />);
    fireEvent.change(screen.getByLabelText(/query/i), { target: { value: 'test' } });
    // Select a model
    fireEvent.mouseDown(screen.getByLabelText(/model/i));
    fireEvent.click(screen.getByRole('option', { name: /gpt-4/i }));
    fireEvent.keyDown(document.activeElement, { key: 'Escape', code: 'Escape' });
    const analyzeButton = await screen.findByRole('button', { name: /analyze/i });
    fireEvent.click(analyzeButton);
    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/analysis/123/processing');
    });
  });

  it('shows Gemma status indicator', async () => {
    renderWithRouter(<AnalysisForm />);
    fireEvent.change(screen.getByLabelText(/query/i), { target: { value: 'test' } });
    // Open the model Autocomplete dropdown
    const modelInput = screen.getByLabelText(/model/i);
    if (modelInput instanceof HTMLElement) {
      fireEvent.mouseDown(modelInput);
    }
    // Look for all Gemma options in the dropdown
    const gemmaOptions = await screen.findAllByRole('option', { name: /gemma/i });
    expect(gemmaOptions.length).toBeGreaterThan(0);
  });

  it('submits the form and navigates to processing page on success', async () => {
    createAnalysisMock.mockResolvedValueOnce({ id: 123 });
    renderWithRouter(<AnalysisForm />);
    // Fill out the form
    fireEvent.change(screen.getByLabelText(/query/i), { target: { value: 'AAPL' } });
    const queryInput = screen.getByLabelText(/query/i);
    if (queryInput instanceof HTMLElement) fireEvent.blur(queryInput);
    fireEvent.mouseDown(screen.getByLabelText(/source/i));
    const redditOptions = screen.getAllByText(/Reddit/i);
    const redditOption = redditOptions.find(el => el.getAttribute && el.getAttribute('role') === 'option');
    if (redditOption) {
      fireEvent.click(redditOption);
    } else {
      fireEvent.click(redditOptions[0]);
    }
    fireEvent.keyDown(document.activeElement, { key: 'Escape', code: 'Escape' });
    const sourceInputs = screen.getAllByLabelText(/source/i);
    const sourceInput = sourceInputs.find(el => el.getAttribute('role') === 'combobox');
    if (sourceInput instanceof HTMLElement) fireEvent.blur(sourceInput);
    fireEvent.mouseDown(screen.getByLabelText(/model/i));
    const vaderOptions = screen.getAllByText(/VADER/i);
    const vaderOption = vaderOptions.find(el => el.getAttribute && el.getAttribute('role') === 'option');
    if (vaderOption) {
      fireEvent.click(vaderOption);
    } else {
      fireEvent.click(vaderOptions[0]);
    }
    fireEvent.keyDown(document.activeElement, { key: 'Escape', code: 'Escape' });
    const modelInputs = screen.getAllByLabelText(/model/i);
    const modelInput = modelInputs.find(el => el.getAttribute('role') === 'combobox');
    if (modelInput instanceof HTMLElement) fireEvent.blur(modelInput);
    // Fill subreddits (Autocomplete)
    const subredditsInputs = screen.getAllByLabelText(/select subreddits/i);
    const subredditsInputEl = subredditsInputs.find(
      el => el.getAttribute('type') === 'text' && el.getAttribute('aria-hidden') !== 'true'
    );
    if (subredditsInputEl instanceof HTMLElement) {
      fireEvent.change(subredditsInputEl, { target: { value: 'wallstreetbets' } });
      fireEvent.keyDown(subredditsInputEl, { key: 'Enter', code: 'Enter' });
      fireEvent.blur(subredditsInputEl);
    }
    // Fill start and end dates if present
    const startDateInputs = screen.queryAllByLabelText(/start date/i);
    const startDateInput = startDateInputs.find(
      el => el.getAttribute('type') === 'text' && el.getAttribute('aria-hidden') !== 'true'
    );
    if (startDateInput instanceof HTMLElement) {
      fireEvent.change(startDateInput, { target: { value: '2024-06-01' } });
      fireEvent.blur(startDateInput);
    }
    const endDateInputs = screen.queryAllByLabelText(/end date/i);
    const endDateInput = endDateInputs.find(
      el => el.getAttribute('type') === 'text' && el.getAttribute('aria-hidden') !== 'true'
    );
    if (endDateInput instanceof HTMLElement) {
      fireEvent.change(endDateInput, { target: { value: '2024-06-02' } });
      fireEvent.blur(endDateInput);
    }
    // Check include_images if present
    const includeImagesCheckbox = screen.queryByLabelText(/include images/i);
    if (includeImagesCheckbox && !(includeImagesCheckbox as HTMLInputElement).checked) {
      fireEvent.click(includeImagesCheckbox);
    }
    // Log all buttons
    const allButtons = screen.getAllByRole('button');
    const submitButton = allButtons.find(btn => /analyze/i.test(btn.textContent || ''));
    if (!submitButton) {
      allButtons.forEach(btn => console.log('Button:', btn.textContent, 'disabled:', (btn as HTMLButtonElement).disabled));
      screen.debug();
      throw new Error('Could not find a button with text "Analyze"');
    }
    expect((submitButton as HTMLButtonElement).disabled).toBe(false);
    console.log('Clicking submit button');
    fireEvent.click(submitButton);
    console.log('Waiting for createAnalysis and navigation to be called');
    // Wait for createAnalysis and navigation to be called
    await waitFor(() => {
      expect(createAnalysisMock).toHaveBeenCalled();
      expect(mockNavigate).toHaveBeenCalledWith('/analysis/123/processing');
    }, { timeout: 2000 });
    console.log('Test completed');
  });

  it('shows error if start date is after end date', async () => {
    renderWithRouter(<AnalysisForm />);
    fireEvent.change(screen.getByLabelText(/query/i), { target: { value: 'AAPL' } });
    // Set start date after end date
    const startDateInputs = screen.queryAllByLabelText(/start date/i);
    const startDateInput = startDateInputs.find(
      el => el.getAttribute('type') === 'text' && el.getAttribute('aria-hidden') !== 'true'
    );
    const endDateInputs = screen.queryAllByLabelText(/end date/i);
    const endDateInput = endDateInputs.find(
      el => el.getAttribute('type') === 'text' && el.getAttribute('aria-hidden') !== 'true'
    );
    if (startDateInput instanceof HTMLElement) {
      fireEvent.change(startDateInput, { target: { value: '2024-06-03' } });
      fireEvent.blur(startDateInput);
    }
    if (endDateInput instanceof HTMLElement) {
      fireEvent.change(endDateInput, { target: { value: '2024-06-02' } });
      fireEvent.blur(endDateInput);
    }
    // Click submit
    const submitButton = screen.getAllByRole('button').find(btn => /analyze/i.test(btn.textContent || ''));
    if (submitButton) {
      fireEvent.click(submitButton);
    }
    // Wait for error message
    const errorAlert = await screen.findByText(/start date must be before end date/i, {}, { timeout: 2000 });
    expect(errorAlert).toBeInTheDocument();
  });

  it('shows validation error if query is empty', async () => {
    renderWithRouter(<AnalysisForm />);
    // Clear the query field if it has a default value
    const queryInput = screen.getByLabelText(/query/i);
    if (queryInput instanceof HTMLElement) {
      fireEvent.change(queryInput, { target: { value: '' } });
      fireEvent.blur(queryInput);
    }
    // Click submit
    const submitButton = screen.getAllByRole('button').find(btn => /analyze/i.test(btn.textContent || ''));
    if (submitButton) {
      fireEvent.click(submitButton);
    }
    // Wait for error message
    const errorAlert = await screen.findByText(/please enter a search query/i, {}, { timeout: 2000 });
    expect(errorAlert).toBeInTheDocument();
  });
}); 