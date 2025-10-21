import React from 'react';
import { Card, CardContent, Typography, TextField, Button, Box, MenuItem, Alert } from '@mui/material';
import { formatCurrency, formatNumber } from '../utils/formatters';

const ScenarioForm = ({ title, fields, baseline, onSubmit }) => {
  const [formData, setFormData] = React.useState({});

  const handleChange = (fieldName, value) => {
    setFormData(prev => ({ ...prev, [fieldName]: value }));
  };

  const handleSubmit = () => {
    onSubmit(formData);
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        
        {baseline && (
          <Alert severity="success" sx={{ mt: 2, mb: 2 }}>
            <Typography variant="body2" fontWeight="bold">Current Baseline (Last 30 Days)</Typography>
            {baseline.current_sessions && (
              <Typography variant="body2">Sessions: {formatNumber(baseline.current_sessions)}</Typography>
            )}
            {baseline.current_cost && (
              <Typography variant="body2">Total Cost: {formatCurrency(baseline.current_cost)}</Typography>
            )}
            {baseline.base_cost && (
              <Typography variant="body2">Base Infrastructure Cost: {formatCurrency(baseline.base_cost)}</Typography>
            )}
          </Alert>
        )}
        
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
          {fields.map((field) => (
            field.type === 'select' ? (
              <TextField
                key={field.name}
                select
                label={field.label}
                value={formData[field.name] || ''}
                onChange={(e) => handleChange(field.name, e.target.value)}
                fullWidth
                size="small"
                helperText={field.helperText}
              >
                {field.options?.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </TextField>
            ) : (
              <TextField
                key={field.name}
                label={field.label}
                type={field.type || 'text'}
                value={formData[field.name] || ''}
                onChange={(e) => handleChange(field.name, e.target.value)}
                fullWidth
                size="small"
                helperText={field.helperText}
              />
            )
          ))}
          <Button variant="contained" onClick={handleSubmit}>
            Calculate Impact
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ScenarioForm;