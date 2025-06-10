import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import AnalysisForm from './AnalysisForm.jsx';
import { createAnalysis, getGemmaStatus } from '../services/api';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { NotificationProvider } from '../contexts/NotificationContext';

// Define mockNavigate at the module level
const mockNavigate = vi.fn();

// Mock useNavigate globally before any tests run
vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal();
  return { ...actual, useNavigate: () => mockNavigate };
});

vi.mock('../services/api');

const renderWithRouter = (ui) => {
  return render(
    <BrowserRouter>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <NotificationProvider>
          {ui}
        </NotificationProvider>
      </LocalizationProvider>
    </BrowserRouter>
  );
};

describe('AnalysisForm', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    getGemmaStatus.mockResolvedValue({ status: 'ready' });
  });

  it('renders form fields', () => {
    renderWithRouter(<AnalysisForm />);
    expect(screen.getByLabelText(/query/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/source/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/model/i)).toBeInTheDocument();
  });

  it('shows validation error if no model selected', async () => {
    renderWithRouter(<AnalysisForm />);
    fireEvent.change(screen.getByLabelText(/query/i), { target: { value: 'test' } });
    fireEvent.click(screen.getByRole('button', { name: /start analysis/i }));
    expect(await screen.findByText(/please select at least one model/i)).toBeInTheDocument();
  });

  it('shows error if backend fails', async () => {
    createAnalysis.mockRejectedValueOnce(new Error('Backend error'));
    renderWithRouter(<AnalysisForm />);
    fireEvent.change(screen.getByLabelText(/query/i), { target: { value: 'test' } });
    // Select a model
    fireEvent.mouseDown(screen.getByLabelText(/model/i));
    fireEvent.click(screen.getByRole('option', { name: /gpt-4/i }));
    fireEvent.keyDown(document.activeElement, { key: 'Escape', code: 'Escape' });
    fireEvent.click(screen.getByRole('button', { name: /start analysis/i }));
    expect(await screen.findByText(/backend error/i)).toBeInTheDocument();
  });

  it('navigates on successful submission', async () => {
    createAnalysis.mockResolvedValueOnce({ id: 123 });
    renderWithRouter(<AnalysisForm />);
    fireEvent.change(screen.getByLabelText(/query/i), { target: { value: 'test' } });
    // Select a model
    fireEvent.mouseDown(screen.getByLabelText(/model/i));
    fireEvent.click(screen.getByRole('option', { name: /gpt-4/i }));
    fireEvent.keyDown(document.activeElement, { key: 'Escape', code: 'Escape' });
    const startButton = await screen.findByRole('button', { name: /start analysis/i });
    fireEvent.click(startButton);
    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/analysis/123/processing');
    });
  });

  it('shows Gemma status indicator', async () => {
    getGemmaStatus.mockResolvedValueOnce({ status: 'ready' });
    renderWithRouter(<AnalysisForm />);
    expect(await screen.findByLabelText(/model/i)).toBeInTheDocument();
    // Open the model select dropdown
    fireEvent.mouseDown(screen.getByLabelText(/model/i));
    // Look for the Gemma option in the dropdown
    const gemmaOption = await screen.findByRole('option', { name: /gemma/i });
    expect(gemmaOption).toBeInTheDocument();
  });

  it('submits the form and navigates to processing page on success', async () => {
    createAnalysis.mockResolvedValue({ id: 123 });
    renderWithRouter(<AnalysisForm />);

    // Fill out the form
    fireEvent.change(screen.getByLabelText(/query/i), { target: { value: 'AAPL' } });
    const queryInput = screen.getByLabelText(/query/i);
    fireEvent.blur(queryInput);
    fireEvent.mouseDown(screen.getByLabelText(/source/i));
    const redditOptions = screen.getAllByText(/Reddit/i);
    const redditOption = redditOptions.find(el => el.getAttribute && el.getAttribute('role') === 'option');
    if (redditOption) {
      fireEvent.click(redditOption);
    } else {
      fireEvent.click(redditOptions[0]);
    }
    // Close the source dropdown and blur
    fireEvent.keyDown(document.activeElement, { key: 'Escape', code: 'Escape' });
    const sourceInputs = screen.getAllByLabelText(/source/i);
    const sourceInput = sourceInputs.find(el => el.getAttribute('role') === 'combobox');
    if (sourceInput) fireEvent.blur(sourceInput);
    // Select model (VADER)
    fireEvent.mouseDown(screen.getByLabelText(/model/i));
    const vaderOptions = screen.getAllByText(/VADER/i);
    const vaderOption = vaderOptions.find(el => el.getAttribute && el.getAttribute('role') === 'option');
    if (vaderOption) {
      fireEvent.click(vaderOption);
    } else {
      fireEvent.click(vaderOptions[0]);
    }
    // Close the model dropdown and blur
    fireEvent.keyDown(document.activeElement, { key: 'Escape', code: 'Escape' });
    const modelInputs = screen.getAllByLabelText(/model/i);
    const modelInput = modelInputs.find(el => el.getAttribute('role') === 'combobox');
    if (modelInput) fireEvent.blur(modelInput);
    // Wait for UI to update
    await waitFor(() => {});
    // Fill subreddits (Autocomplete)
    const subredditsInputs = screen.getAllByLabelText(/select subreddits/i);
    const subredditsInputEl = subredditsInputs.find(
      el => el.getAttribute('type') === 'text' && el.getAttribute('aria-hidden') !== 'true'
    );
    if (subredditsInputEl) {
      fireEvent.change(subredditsInputEl, { target: { value: 'wallstreetbets' } });
      fireEvent.keyDown(subredditsInputEl, { key: 'Enter', code: 'Enter' });
      fireEvent.blur(subredditsInputEl);
    }
    // Fill start and end dates if present
    const startDateInputs = screen.queryAllByLabelText(/start date/i);
    const startDateInput = startDateInputs.find(
      el => el.getAttribute('type') === 'text' && el.getAttribute('aria-hidden') !== 'true'
    );
    if (startDateInput) {
      fireEvent.change(startDateInput, { target: { value: '2024-06-01' } });
    }
    const endDateInputs = screen.queryAllByLabelText(/end date/i);
    const endDateInput = endDateInputs.find(
      el => el.getAttribute('type') === 'text' && el.getAttribute('aria-hidden') !== 'true'
    );
    if (endDateInput) {
      fireEvent.change(endDateInput, { target: { value: '2024-06-02' } });
    }
    // Check include_images if present
    const includeImagesCheckbox = screen.queryByLabelText(/include images/i);
    if (includeImagesCheckbox && !includeImagesCheckbox.checked) {
      fireEvent.click(includeImagesCheckbox);
    }
    // Log all buttons
    const allButtons = screen.getAllByRole('button');
    const submitButton = allButtons.find(btn => /start|submit/i.test(btn.textContent || ''));
    if (!submitButton) {
      allButtons.forEach(btn => console.log('Button:', btn.textContent, 'disabled:', btn.disabled));
      screen.debug();
      throw new Error('Could not find a button with text "Start" or "Submit"');
    }
    expect(submitButton).toBeEnabled();
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(createAnalysis).toHaveBeenCalled();
      expect(mockNavigate).toHaveBeenCalledWith('/analysis/123/processing');
      expect(screen.queryByText(/failed to create analysis/i)).not.toBeInTheDocument();
    });
  });
}); 