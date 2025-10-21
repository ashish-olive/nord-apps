import React from 'react';
import { Card, CardContent, Typography, Box, Chip } from '@mui/material';
import { formatNumber, formatPercent, formatLatency, getTrendColor, getTrendIcon } from '../utils/formatters';

const KPICard = ({ title, value, unit = '', change, format = 'number', color = 'primary', icon }) => {
  const formatValue = (val) => {
    switch (format) {
      case 'percent':
        return formatPercent(val);
      case 'latency':
        return formatLatency(val);
      case 'number':
        return formatNumber(val);
      default:
        return val;
    }
  };

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="body2" sx={{ fontWeight: 600, color: '#666666', flex: 1 }}>
            {title}
          </Typography>
          {icon && (
            <Box sx={{ 
              color: `${color}.main`, 
              display: 'flex', 
              alignItems: 'center',
              ml: 1,
              fontSize: '1.25rem'
            }}>
              {icon}
            </Box>
          )}
        </Box>
        <Typography variant="h4" component="div" sx={{ mb: 1, color: '#000000', fontWeight: 700 }}>
          {formatValue(value)}{unit}
        </Typography>
        {change !== undefined && change !== null && (
          <Chip
            label={`${getTrendIcon(change)} ${formatPercent(Math.abs(change))}`}
            size="small"
            sx={{
              bgcolor: getTrendColor(change),
              color: 'white',
              fontWeight: 'bold',
            }}
          />
        )}
      </CardContent>
    </Card>
  );
};

export default KPICard;
