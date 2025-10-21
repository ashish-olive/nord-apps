import React from 'react';
import { Card, CardContent, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Chip } from '@mui/material';
import { formatNumber, formatLatency, formatPercent, getPerformanceColor } from '../utils/formatters';

const ServerTable = ({ servers, title = "Top Performing Servers" }) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ color: '#000000', fontWeight: 600 }}>
          {title}
        </Typography>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Server</TableCell>
                <TableCell>Location</TableCell>
                <TableCell>Provider</TableCell>
                <TableCell align="right">Sessions</TableCell>
                <TableCell align="right">Avg Latency</TableCell>
                <TableCell align="right">Nonet Rate</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {servers.map((server, index) => (
                <TableRow key={index}>
                  <TableCell>{server.hostname}</TableCell>
                  <TableCell>{server.location}</TableCell>
                  <TableCell>{server.provider}</TableCell>
                  <TableCell align="right">{formatNumber(server.session_count)}</TableCell>
                  <TableCell align="right">
                    <Chip 
                      label={formatLatency(server.avg_latency_ms)} 
                      size="small"
                      color={server.avg_latency_ms < 2000 ? 'success' : 'warning'}
                    />
                  </TableCell>
                  <TableCell align="right">
                    <Chip 
                      label={formatPercent(server.nonet_rate)} 
                      size="small"
                      color={getPerformanceColor(100 - server.nonet_rate, 90)}
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </CardContent>
    </Card>
  );
};

export default ServerTable;
