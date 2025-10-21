import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { formatCurrency } from '../utils/formatters';

const LocationCostChart = ({ data, title = 'Usage by Location' }) => {
  const chartData = data.slice(0, 10).map(item => ({
    location: item.location,
    cost: item.total_cost,
    sessions: item.total_sessions,
  }));

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={chartData} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" tickFormatter={(value) => `$${value}`} />
            <YAxis dataKey="location" type="category" width={150} />
            <Tooltip formatter={(value) => formatCurrency(value)} />
            <Legend />
            <Bar dataKey="cost" fill="#1976d2" name="Total Usage" />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};

export default LocationCostChart;