import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import DashboardIcon from '@mui/icons-material/Dashboard';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import ScienceIcon from '@mui/icons-material/Science';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { path: '/executive', label: 'Executive', icon: <DashboardIcon /> },
    { path: '/usage-analysis', label: 'Usage Analysis', icon: <AnalyticsIcon /> },
    { path: '/scenarios', label: 'Scenarios', icon: <ScienceIcon /> },
  ];

  return (
    <AppBar position="fixed">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 0, mr: 4 }}>
          Usage Analytics
        </Typography>
        <Box sx={{ flexGrow: 1, display: 'flex', gap: 1 }}>
          {navItems.map((item) => (
            <Button
              key={item.path}
              color="inherit"
              startIcon={item.icon}
              onClick={() => navigate(item.path)}
              sx={{
                borderBottom: location.pathname === item.path ? '2px solid white' : 'none',
                borderRadius: 0,
              }}
            >
              {item.label}
            </Button>
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;