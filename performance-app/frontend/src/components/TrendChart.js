import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const TrendChart = ({ data }) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ color: '#000000', fontWeight: 600 }}>
          Performance Trends Over Time
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tick={{ fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis 
              yAxisId="left" 
              label={{ value: 'Connectivity Rate (%)', angle: -90, position: 'insideLeft' }}
              domain={[90, 100]}
            />
            <YAxis 
              yAxisId="right" 
              orientation="right" 
              label={{ value: 'Latency (ms)', angle: 90, position: 'insideRight' }}
            />
            <Tooltip />
            <Legend />
            <Line 
              yAxisId="left" 
              type="monotone" 
              dataKey="connectivity_rate" 
              stroke="#4caf50" 
              strokeWidth={2}
              name="Connectivity Rate (%)" 
              dot={{ r: 3 }}
            />
            <Line 
              yAxisId="right" 
              type="monotone" 
              dataKey="avg_latency_ms" 
              stroke="#2196f3" 
              strokeWidth={2}
              name="Avg Latency (ms)" 
              dot={{ r: 3 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};

export default TrendChart;
