import React, { useState, useEffect } from 'react';
import { Container, Grid, Typography, CircularProgress, Box } from '@mui/material';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import PeopleIcon from '@mui/icons-material/People';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import KPICard from '../components/KPICard';
import UsageTrendChart from '../components/UsageTrendChart';
import ProviderBreakdownChart from '../components/ProviderBreakdownChart';
import ServerTable from '../components/ServerTable';
import { usageApi } from '../api/usageApi';

const ExecutiveDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState(null);
  const [trends, setTrends] = useState([]);
  const [providers, setProviders] = useState([]);
  const [topServers, setTopServers] = useState([]);
  const days = 30;

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [summaryRes, trendsRes, providersRes, serversRes] = await Promise.all([
        usageApi.getExecutiveSummary(days),
        usageApi.getCostTrends(days),
        usageApi.getCostByProvider(days),
        usageApi.getCostByServer(days, 10),
      ]);

      setSummary(summaryRes.data.metrics);
      setTrends(trendsRes.data.trends);
      setProviders(providersRes.data.providers);
      setTopServers(serversRes.data.servers);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
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
        Executive Dashboard
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
        Last {days} days overview
      </Typography>

      <Grid container spacing={3}>
        {/* KPI Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Total Usage"
            value={summary?.total_cost?.value}
            change={summary?.total_cost?.change_percent}
            format="currency"
            icon={<AttachMoneyIcon />}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Usage per Session"
            value={summary?.cost_per_session?.value}
            change={summary?.cost_per_session?.change_percent}
            format="currency"
            icon={<TrendingUpIcon />}
            infoText="Total infrastructure usage divided by number of VPN sessions. Includes both base server usage and data transfer usage."
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Total Sessions"
            value={summary?.total_sessions}
            format="number"
            icon={<PeopleIcon />}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Total Hours"
            value={summary?.total_hours}
            format="number"
            icon={<CalendarTodayIcon />}
          />
        </Grid>

        {/* Usage Trend Chart */}
        <Grid item xs={12} md={8}>
          <UsageTrendChart data={trends} title="Daily Usage Trends" />
        </Grid>

        {/* Provider Breakdown */}
        <Grid item xs={12} md={4}>
          <ProviderBreakdownChart data={providers} />
        </Grid>

        {/* Top Usage Servers */}
        <Grid item xs={12}>
          <ServerTable data={topServers} />
        </Grid>
      </Grid>
    </Container>
  );
};

export default ExecutiveDashboard;