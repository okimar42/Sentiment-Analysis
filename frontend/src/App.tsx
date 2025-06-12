import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AnalysisForm from './pages/AnalysisForm';
import AnalysisResults from './pages/AnalysisResults';
import AnalysisProcessing from './pages/AnalysisProcessing';
import Layout from './components/Layout';

function App() {
  return (
    <BrowserRouter>
              <Routes>
        <Route path="/" element={<Layout />}>
                  <Route index element={<Dashboard />} />
                  <Route path="new-analysis" element={<AnalysisForm />} />
                  <Route path="results/:id" element={<AnalysisResults />} />
                  <Route path="analysis/:id/processing" element={<AnalysisProcessing />} />
                  <Route path="analysis/:id" element={<AnalysisResults />} />
                  <Route path="login" element={<Login />} />
                </Route>
              </Routes>
            </BrowserRouter>
  );
}

export default App;
