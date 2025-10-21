export const formatCurrency = (value) => {
  if (value === null || value === undefined) return '$0.00';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
};

export const formatNumber = (value, decimals = 0) => {
  if (value === null || value === undefined) return '0';
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
};

export const formatPercent = (value, decimals = 1) => {
  if (value === null || value === undefined) return '0%';
  return `${formatNumber(value, decimals)}%`;
};

export const formatCompactNumber = (value) => {
  if (value === null || value === undefined) return '0';
  if (value >= 1000000) {
    return `${(value / 1000000).toFixed(1)}M`;
  }
  if (value >= 1000) {
    return `${(value / 1000).toFixed(1)}K`;
  }
  return value.toString();
};

export const getTrendColor = (value) => {
  if (value > 0) return 'error.main';
  if (value < 0) return 'success.main';
  return 'text.secondary';
};

export const getTrendIcon = (value) => {
  if (value > 0) return '↑';
  if (value < 0) return '↓';
  return '→';
};