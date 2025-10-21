import React, { useState, useEffect } from 'react';
import { Container, Grid, Typography, CircularProgress, Box, FormControl, Select, MenuItem } from '@mui/material';
import SignalCellularAltIcon from '@mui/icons-material/SignalCellularAlt';
import SpeedIcon from '@mui/icons-material/Speed';
import NetworkCheckIcon from '@mui/icons-material/NetworkCheck';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import RefreshIcon from '@mui/icons-material/Refresh';
import LinkOffIcon from '@mui/icons-material/LinkOff';
import KPICard from '../components/KPICard';
import ProtocolChart from '../components/ProtocolChart';
import TrendChart from '../components/TrendChart';
import ServerTable from '../components/ServerTable';
import { performanceApi } from '../api/performanceApi';

const PerformanceDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [connectivity, setConnectivity] = useState(null);
  const [latency, setLatency] = useState(null);
  const [quality, setQuality] = useState(null);
  const [satisfaction, setSatisfaction] = useState(null);
  const [protocols, setProtocols] = useState([]);
  const [topServers, setTopServers] = useState([]);
  const [trends, setTrends] = useState([]);
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
      const [connRes, latRes, qualRes, satRes, protRes, servRes, trendRes] = await Promise.all([
        performanceApi.getConnectivitySummary(days),
        performanceApi.getLatencyMetrics(days),
        performanceApi.getQualityMetrics(days),
        performanceApi.getUserSatisfaction(days),
        performanceApi.getPerformanceByProtocol(days),
        performanceApi.getPerformanceByServer(days, 10),
        performanceApi.getPerformanceTrends(days),
      ]);

      setConnectivity(connRes.data.metrics);
      setLatency(latRes.data.metrics);
      setQuality(qualRes.data.metrics);
      setSatisfaction(satRes.data.metrics);
      setProtocols(protRes.data.protocols);
      setTopServers(servRes.data.servers);
      setTrends(trendRes.data.trends);
    } catch (error) {
      console.error('Error loading performance data:', error);
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
          Performance Dashboard
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
        {timeframes.find(tf => tf.value === days)?.label} performance metrics
      </Typography>

      <Grid container spacing={3}>
        {/* Row 1: First 4 KPI Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Connectivity Rate"
            value={connectivity?.connectivity_rate?.value}
            format="percent"
            color="success"
            icon={<SignalCellularAltIcon />}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Avg Connection Time"
            value={latency?.average_latency_ms}
            format="latency"
            color="primary"
            icon={<SpeedIcon />}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Network Quality"
            value={100 - quality?.nonet_rate?.value}
            format="percent"
            color="info"
            icon={<NetworkCheckIcon />}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="User Satisfaction"
            value={satisfaction?.satisfaction_rate?.value}
            format="percent"
            color="warning"
            icon={<ThumbUpIcon />}
          />
        </Grid>

        {/* Row 2: Remaining 3 KPI Cards (will be 4 per row on large screens) */}
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Nonet Sessions Rate"
            value={quality?.nonet_rate?.value}
            format="percent"
            color="error"
            icon={<ErrorOutlineIcon />}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Total Reconnects"
            value={quality?.total_reconnects}
            format="number"
            color="warning"
            icon={<RefreshIcon />}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Unexpected Disconnects"
            value={quality?.unexpected_disconnects}
            format="number"
            color="error"
            icon={<LinkOffIcon />}
          />
        </Grid>

        {/* Force new row for table */}
        <Grid item xs={12} sx={{ height: 0 }} />

        {/* Row 3: Top Performing Servers Table - Full Width */}
        <Grid item xs={12}>
          <ServerTable servers={topServers} title="Top 10 Performing Servers (by Latency)" />
        </Grid>

        {/* Row 4: Charts Side by Side */}
        <Grid item xs={12} md={6}>
          <TrendChart data={trends} />
        </Grid>
        <Grid item xs={12} md={6}>
          <ProtocolChart data={protocols} />
        </Grid>
      </Grid>
    </Container>
  );
};

export default PerformanceDashboard;
