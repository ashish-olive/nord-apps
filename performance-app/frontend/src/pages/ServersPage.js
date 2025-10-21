import React, { useState, useEffect } from 'react';
import { Container, Grid, Typography, CircularProgress, Box, FormControl, Select, MenuItem } from '@mui/material';
import ServerTable from '../components/ServerTable';
import { performanceApi } from '../api/performanceApi';

const ServersPage = () => {
  const [loading, setLoading] = useState(true);
  const [servers, setServers] = useState([]);
  const [days, setDays] = useState(30);

  const timeframes = [
    { value: 1, label: 'Last 24 Hours' },
    { value: 7, label: 'Last 7 Days' },
    { value: 30, label: 'Last 30 Days' },
    { value: 90, label: 'Last 90 Days' },
    { value: 365, label: 'Last Year' },
  ];

  useEffect(() => {
    loadData();
  }, [days]);

  const loadData = async () => {
    try {
      setLoading(true);
      const response = await performanceApi.getPerformanceByServer(days, 50);
      setServers(response.data.servers);
    } catch (error) {
      console.error('Error loading server data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="xl">
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 3, mb: 1 }}>
        <Typography variant="h4" sx={{ color: '#000000', fontWeight: 700 }}>
          Server Performance
        </Typography>
        <FormControl size="small" sx={{ minWidth: 180 }}>
          <Select
            value={days}
            onChange={(e) => setDays(e.target.value)}
            sx={{ bgcolor: 'white' }}
          >
            {timeframes.map((tf) => (
              <MenuItem key={tf.value} value={tf.value}>
                {tf.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>
      <Typography variant="body1" gutterBottom sx={{ mb: 3, color: '#666666' }}>
        Detailed performance metrics for all VPN servers ({timeframes.find(tf => tf.value === days)?.label})
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <ServerTable servers={servers} title="All Servers Performance" />
        </Grid>
      </Grid>
    </Container>
  );
};

export default ServersPage;
