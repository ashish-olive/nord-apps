import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';
import Navbar from './components/Navbar';
import ExecutiveDashboard from './pages/ExecutiveDashboard';
import CostAnalysisDashboard from './pages/CostAnalysisDashboard';
import ScenarioStudio from './pages/ScenarioStudio';

function App() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
        <Routes>
          <Route path="/" element={<Navigate to="/executive" replace />} />
          <Route path="/executive" element={<ExecutiveDashboard />} />
          <Route path="/cost-analysis" element={<CostAnalysisDashboard />} />
          <Route path="/scenarios" element={<ScenarioStudio />} />
        </Routes>
      </Box>
    </Box>
  );
}

export default App;