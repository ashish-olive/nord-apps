export const formatNumber = (num) => {
  if (num === null || num === undefined) return '0';
  return new Intl.NumberFormat('en-US').format(Math.round(num));
};

export const formatPercent = (num, decimals = 2) => {
  if (num === null || num === undefined) return '0%';
  return `${num.toFixed(decimals)}%`;
};

export const formatLatency = (ms) => {
  if (ms === null || ms === undefined) return '0ms';
  if (ms < 1000) return `${Math.round(ms)}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
};

export const formatDuration = (seconds) => {
  if (!seconds) return '0m';
  const minutes = Math.round(seconds / 60);
  if (minutes < 60) return `${minutes}m`;
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  return `${hours}h ${remainingMinutes}m`;
};

export const getTrendColor = (value) => {
  if (value > 0) return '#4caf50';
  if (value < 0) return '#f44336';
  return '#9e9e9e';
};

export const getTrendIcon = (value) => {
  if (value > 0) return '↑';
  if (value < 0) return '↓';
  return '→';
};

export const getPerformanceColor = (rate, threshold = 95) => {
  if (rate >= threshold) return 'success';
  if (rate >= threshold - 5) return 'warning';
  return 'error';
};
