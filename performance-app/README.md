# Surfshark VPN Performance Analytics

Real-time performance monitoring and quality metrics for VPN infrastructure.

## Features

### Primary Metrics (Based on Surfshark's Actual Schema)
1. **Connectivity Rate** - Connection success rate (most important KPI)
2. **Latency Metrics** - Average, median, and P95 connection times
3. **Network Quality** - Nonet rate, reconnects, unexpected disconnects
4. **User Satisfaction** - Positive/negative rating metrics

### Analysis Dimensions
- **By Protocol** - WireGuard, OpenVPN, IKEv2, NordLynx performance comparison
- **By Server** - Top/bottom performing servers
- **By Location** - Geographic performance analysis
- **By Provider** - Cloud provider performance (AWS, Azure, Google Cloud, etc.)

## Backend API

### Start the API
```bash
cd /Users/ashsharma/Documents/Nord\ Apps\ POC/surfshark-vpn-analytics
source venv/bin/activate
python performance-app/backend/app.py
```

API runs on **http://localhost:5003**

### API Endpoints

#### Core Metrics
- `GET /api/performance/connectivity/summary?days=30` - Connectivity rate
- `GET /api/performance/latency?days=30` - Connection latency metrics
- `GET /api/performance/quality?days=30` - Network quality metrics
- `GET /api/performance/user-satisfaction?days=30` - User ratings

#### Analysis
- `GET /api/performance/by-protocol?days=30` - Performance by protocol
- `GET /api/performance/by-server?days=30&limit=20` - Server performance
- `GET /api/performance/by-location?days=30` - Location performance

#### Utility
- `GET /api/health` - Health check
- `GET /api/providers` - List cloud providers

## Architecture

### Shared Database
- Uses the same SQLite database as Cost Analytics
- Single source of truth for all VPN session data
- No data duplication

### Key Performance Fields
```python
# VPNSession model includes:
- connecting_time_ms          # Connection latency
- connect_intent_trigger      # How connection was initiated
- disconnect_intent_trigger   # Why session ended
- nonet_event_count          # Network interruptions
- reconnect_event_count      # Stability issues
- unexpected_disconnect      # Reliability problems
- has_user_rating            # User feedback
- is_negative_rating         # Satisfaction indicator
```

## Data Flow

1. **VPN Sessions** → Generated with realistic performance metrics
2. **Performance Repository** → Aggregates metrics from sessions
3. **Flask API** → Exposes REST endpoints
4. **React Frontend** → Visualizes performance data

## Next Steps

1. Build React frontend dashboards
2. Add real-time monitoring alerts
3. Implement SLA tracking
4. Add performance trend analysis
