import React from 'react';
import { Card, CardContent, Typography, Grid, Box, Chip, Alert, Divider, Tooltip, IconButton } from '@mui/material';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import { formatCurrency, formatPercent } from '../utils/formatters';

const ScenarioResult = ({ result }) => {
  if (!result) return null;

  const getRecommendationColor = (rec) => {
    if (rec === 'Proceed' || rec === 'Implement') return 'success';
    if (rec === 'Review' || rec === 'Monitor') return 'warning';
    return 'error';
  };
  
  const getAlertSeverity = (rec) => {
    if (rec === 'Proceed' || rec === 'Implement') return 'success';
    if (rec === 'Review' || rec === 'Monitor') return 'info';
    return 'warning';
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Scenario Results
        </Typography>
        
        <Box sx={{ mb: 2 }}>
          <Chip 
            label={result.recommendation}
            color={getRecommendationColor(result.recommendation)}
            sx={{ fontWeight: 'bold' }}
          />
        </Box>

        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="text.secondary">
              Baseline Cost
            </Typography>
            <Typography variant="h5">
              {formatCurrency(result.baseline?.total_cost)}
            </Typography>
          </Grid>
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="text.secondary">
              Projected Cost
            </Typography>
            <Typography variant="h5">
              {formatCurrency(result.projected?.total_cost)}
            </Typography>
          </Grid>
          {result.projected?.cost_change_percent !== undefined && (
            <Grid item xs={12}>
              <Typography variant="subtitle2" color="text.secondary">
                Cost Change
              </Typography>
              <Typography variant="h6" color={result.projected.cost_change_percent > 0 ? 'error' : 'success'}>
                {formatPercent(result.projected.cost_change_percent)}
              </Typography>
            </Grid>
          )}
          {result.projected?.savings !== undefined && (
            <Grid item xs={12}>
              <Typography variant="subtitle2" color="text.secondary">
                {result.projected.savings >= 0 ? 'Total Savings' : 'Additional Cost'}
              </Typography>
              <Typography variant="h6" color={result.projected.savings >= 0 ? 'success.main' : 'error.main'}>
                {formatCurrency(Math.abs(result.projected.savings))}
              </Typography>
            </Grid>
          )}
        </Grid>
        
        {result.explanation && (
          <>
            <Divider sx={{ my: 2 }} />
            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
              Analysis
            </Typography>
            <Typography variant="body2" paragraph>
              {result.explanation}
            </Typography>
          </>
        )}
        
        {result.rationale && (
          <Alert severity={getAlertSeverity(result.recommendation)} sx={{ mt: 2 }}>
            <Typography variant="body2" fontWeight="bold">Why {result.recommendation}?</Typography>
            <Typography variant="body2" sx={{ mt: 0.5 }}>
              {result.rationale}
            </Typography>
          </Alert>
        )}
        
        {result.details && result.details.length > 0 && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
              Key Considerations
            </Typography>
            <Box component="ul" sx={{ mt: 1, pl: 2 }}>
              {result.details.map((detail, index) => {
                // Add info tooltip for infrastructure scaling factor
                const isScalingFactor = detail.includes('Infrastructure scaling factor');
                const isEffectiveSavings = detail.includes('effective savings');
                
                return (
                  <Box component="li" key={index} sx={{ mb: 0.5, display: 'flex', alignItems: 'center' }}>
                    <Typography variant="body2" component="span">
                      {detail}
                    </Typography>
                    {isScalingFactor && (
                      <Tooltip 
                        title="Infrastructure doesn't scale 1:1 with traffic due to economies of scale, better utilization, and shared resources. A 70% factor means 10% traffic growth requires ~7% more infrastructure."
                        arrow
                        placement="top"
                      >
                        <IconButton size="small" sx={{ ml: 0.5, p: 0.25 }}>
                          <InfoOutlinedIcon fontSize="small" sx={{ color: 'info.main' }} />
                        </IconButton>
                      </Tooltip>
                    )}
                    {isEffectiveSavings && (
                      <Tooltip 
                        title="Effective savings account for the percentage of infrastructure where this optimization applies. For example, reserved instances only affect compute costs (~60% of total), and spot instances only work for ~30% of workloads."
                        arrow
                        placement="top"
                      >
                        <IconButton size="small" sx={{ ml: 0.5, p: 0.25 }}>
                          <InfoOutlinedIcon fontSize="small" sx={{ color: 'info.main' }} />
                        </IconButton>
                      </Tooltip>
                    )}
                  </Box>
                );
              })}
            </Box>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default ScenarioResult;