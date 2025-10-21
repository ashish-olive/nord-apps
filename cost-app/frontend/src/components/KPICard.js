import React from 'react';
import { Card, CardContent, Typography, Box, Chip, Tooltip, IconButton } from '@mui/material';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import { formatCurrency, formatNumber, formatPercent, getTrendColor, getTrendIcon } from '../utils/formatters';

const InfoTooltip = ({ title, children }) => (
  <Tooltip title={title}>
    <IconButton>
      <InfoOutlinedIcon />
    </IconButton>
  </Tooltip>
);

const KPICard = ({ title, value, change, format = 'currency', icon, infoTooltip }) => {
  const formatValue = (val) => {
    switch (format) {
      case 'currency':
        return formatCurrency(val);
      case 'number':
        return formatNumber(val);
      case 'percent':
        return formatPercent(val);
      default:
        return val;
    }
  };

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography color="text.secondary" variant="body2">
            {title}
          </Typography>
          {icon && <Box sx={{ color: 'primary.main' }}>{icon}</Box>}
        </Box>
        <Typography variant="h4" component="div" sx={{ mb: 1 }}>
          {formatValue(value)}
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