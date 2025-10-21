import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import SpeedIcon from '@mui/icons-material/Speed';

const Navbar = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <SpeedIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Performance Analytics
        </Typography>
        <Box>
          <Button color="inherit" component={RouterLink} to="/">
            Dashboard
          </Button>
          <Button color="inherit" component={RouterLink} to="/servers">
            Servers
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
