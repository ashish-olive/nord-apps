import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import { formatCurrency, formatNumber } from '../utils/formatters';

const ServerTable = ({ data, title = 'Top Usage Servers' }) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Hostname</TableCell>
                <TableCell>Location</TableCell>
                <TableCell>Provider</TableCell>
                <TableCell align="right">Total Usage</TableCell>
                <TableCell align="right">Sessions</TableCell>
                <TableCell align="right">Usage/Session</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((server, index) => (
                <TableRow key={index}>
                  <TableCell>{server.hostname}</TableCell>
                  <TableCell>{server.location}</TableCell>
                  <TableCell>{server.provider}</TableCell>
                  <TableCell align="right">{formatCurrency(server.total_cost)}</TableCell>
                  <TableCell align="right">{formatNumber(server.total_sessions)}</TableCell>
                  <TableCell align="right">{formatCurrency(server.cost_per_session)}</TableCell>
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