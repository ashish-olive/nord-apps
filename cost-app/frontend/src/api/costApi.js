import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5002';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const costApi = {
  // Executive Dashboard
  getExecutiveSummary: (days = 30) => 
    api.get(`/api/cost/executive/summary?days=${days}`),
  
  getCostTrends: (days = 30) => 
    api.get(`/api/cost/trends?days=${days}`),
  
  // Cost Analysis
  getCostByProvider: (days = 30) => 
    api.get(`/api/cost/by-provider?days=${days}`),
  
  getCostByLocation: (days = 30) => 
    api.get(`/api/cost/by-location?days=${days}`),
  
  getCostByServer: (days = 30, limit = 10) => 
    api.get(`/api/cost/by-server?days=${days}&limit=${limit}`),
  
  getServerUtilization: (days = 30, limit = 20) => 
    api.get(`/api/servers/utilization?days=${days}&limit=${limit}`),
  
  // Providers
  getProviders: () => 
    api.get('/api/providers'),
  
  // Health check
  healthCheck: () => 
    api.get('/api/health'),
};

export default costApi;