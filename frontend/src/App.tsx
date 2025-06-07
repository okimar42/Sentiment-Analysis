import React, { useState, useMemo } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import Layout from './components/Layout.tsx';
import Dashboard from './pages/Dashboard.tsx';
import AnalysisForm from './pages/AnalysisForm.tsx';
import AnalysisResults from './pages/AnalysisResults.tsx';
import Login from './pages/Login.tsx';
import AnalysisProcessing from './pages/AnalysisProcessing.tsx';

const App: React.FC = () => {
  const [mode, setMode] = useState<'light' | 'dark'>('light');
  const toggleMode = () => setMode((prev) => (prev === 'light' ? 'dark' : 'light'));
  const theme = useMemo(() => createTheme({
    palette: {
      mode,
      primary: {
        main: '#1976d2',
      },
      secondary: {
        main: '#dc004e',
      },
    },
  }), [mode]);

  return (
    <ThemeProvider theme={theme}>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <CssBaseline />
        <Router>
          <Layout mode={mode} toggleMode={toggleMode}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/login" element={<Login />} />
              <Route path="/new-analysis" element={<AnalysisForm />} />
              <Route path="/analysis/:id/processing" element={<AnalysisProcessing />} />
              <Route path="/analysis/:id" element={<AnalysisResults />} />
            </Routes>
          </Layout>
        </Router>
      </LocalizationProvider>
    </ThemeProvider>
  );
}

export default App;
