import React, { useState, useEffect } from 'react';
import { Container, Grid, Typography, CircularProgress, Box } from '@mui/material';
import LocationCostChart from '../components/LocationCostChart';
import ProviderBreakdownChart from '../components/ProviderBreakdownChart';
import ServerTable from '../components/ServerTable';
import { costApi } from '../api/costApi';

const CostAnalysisDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [providers, setProviders] = useState([]);
  const [locations, setLocations] = useState([]);
  const [topServers, setTopServers] = useState([]);
  const days = 30;

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [providersRes, locationsRes, serversRes] = await Promise.all([
        costApi.getCostByProvider(days),
        costApi.getCostByLocation(days),
        costApi.getCostByServer(days, 20),
      ]);

      setProviders(providersRes.data.providers);
      setLocations(locationsRes.data.locations);
      setTopServers(serversRes.data.servers);
    } catch (error) {
      console.error('Error loading usage analysis data:', error);
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
      <Typography variant="h4" gutterBottom>
        Usage Analysis Dashboard
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
        Detailed usage breakdown and analysis
      </Typography>

      <Grid container spacing={3}>
        {/* Provider Breakdown */}
        <Grid item xs={12} md={6}>
          <ProviderBreakdownChart data={providers} />
        </Grid>

        {/* Location Breakdown */}
        <Grid item xs={12} md={6}>
          <LocationCostChart data={locations} />
        </Grid>

        {/* Top Usage Servers */}
        <Grid item xs={12}>
          <ServerTable data={topServers} title="Top 20 Usage Servers" />
        </Grid>
      </Grid>
    </Container>
  );
};

export default CostAnalysisDashboard;