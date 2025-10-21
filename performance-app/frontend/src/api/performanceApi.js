import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5003/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const performanceApi = {
  // Connectivity metrics
  getConnectivitySummary: (days = 30) => 
    api.get(`/performance/connectivity/summary?days=${days}`),
  
  // Latency metrics
  getLatencyMetrics: (days = 30) => 
    api.get(`/performance/latency?days=${days}`),
  
  // Quality metrics
  getQualityMetrics: (days = 30) => 
    api.get(`/performance/quality?days=${days}`),
  
  // User satisfaction
  getUserSatisfaction: (days = 30) => 
    api.get(`/performance/user-satisfaction?days=${days}`),
  
  // Performance by protocol
  getPerformanceByProtocol: (days = 30) => 
    api.get(`/performance/by-protocol?days=${days}`),
  
  // Performance by server
  getPerformanceByServer: (days = 30, limit = 20) => 
    api.get(`/performance/by-server?days=${days}&limit=${limit}`),
  
  // Performance by location
  getPerformanceByLocation: (days = 30) => 
    api.get(`/performance/by-location?days=${days}`),
  
  // Performance trends over time
  getPerformanceTrends: (days = 30) => 
    api.get(`/performance/trends?days=${days}`),
  
  // Providers
  getProviders: () => 
    api.get('/providers'),
};
