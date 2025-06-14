import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { themes } from './themes';
import type { ThemeKey } from './themes';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AnalysisForm from './pages/AnalysisForm';
import AnalysisResults from './pages/AnalysisResults';
import AnalysisProcessing from './pages/AnalysisProcessing';
import Layout from './components/Layout';
import { NotificationProvider } from './contexts/NotificationContext';

function App() {
  const [selectedTheme, setSelectedTheme] = useState<ThemeKey>('gruvboxDark');

  return (
    <ThemeProvider theme={themes[selectedTheme]}>
      <NotificationProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Layout selectedTheme={selectedTheme} setSelectedTheme={setSelectedTheme} />}> 
              <Route index element={<Dashboard />} />
              <Route path="new-analysis" element={<AnalysisForm />} />
              <Route path="results/:id" element={<AnalysisResults />} />
              <Route path="analysis/:id/processing" element={<AnalysisProcessing />} />
              <Route path="analysis/:id" element={<AnalysisResults />} />
              <Route path="login" element={<Login />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </NotificationProvider>
    </ThemeProvider>
  );
}

export default App;
