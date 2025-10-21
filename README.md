# Surfshark VPN Analytics Platform

A comprehensive analytics platform for VPN infrastructure with **two integrated applications**: Usage Analytics and Performance Analytics, sharing a unified database.

## 🚀 Features

### 💰 Usage Analytics App (Port 3000)
**Executive Dashboard**
- Real-time usage KPIs with period-over-period comparisons
- Daily usage trend visualization
- Provider usage breakdown
- Top usage servers analysis

**Usage Analysis Dashboard**
- Usage breakdown by cloud provider (AWS, GCP, Azure, DigitalOcean, Vultr)
- Geographic usage distribution
- Detailed server-level usage analysis
- Session and utilization metrics

**Scenario Studio**
- **Server Scaling**: Model usage impact of adding/removing servers
- **Provider Migration**: Calculate savings from provider changes
- **Traffic Growth**: Forecast usage with traffic increases
- **Usage Optimization**: Estimate savings from optimization initiatives

### 📊 Performance Analytics App (Port 3001)
**Performance Dashboard**
- **Connectivity Rate**: Connection success rate (PRIMARY KPI)
- **Latency Metrics**: Average connection time with trends
- **Network Quality**: Nonet rate, reconnects, unexpected disconnects
- **User Satisfaction**: Positive/negative rating metrics
- **Historical Trends**: Performance over time visualization
- **Protocol Comparison**: WireGuard vs OpenVPN vs IKEv2 vs NordLynx

**Server Performance**
- Top/bottom performing servers by latency
- Geographic performance analysis
- Provider performance comparison
- Detailed server metrics table

## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React 18** - UI framework
- **Material-UI (MUI) v5** - Component library
- **Recharts** - Data visualization
- **React Router** - Navigation
- **Axios** - HTTP client

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+ and npm
- 2-8 GB RAM (depending on dataset size)
- 1-5 GB disk space (depending on dataset size)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd surfshark-vpn-analytics
```

### 2. Set Up Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies (Both Apps)

**Usage Analytics Frontend:**
```bash
cd surfshark-vpn-analytics/cost-app/frontend
npm install
cd ../../..
```

**Performance Analytics Frontend:**
```bash
cd surfshark-vpn-analytics/performance-app/frontend
npm install
cd ../../..
```

## 📊 Data Generation

**⚠️ IMPORTANT:** The database is NOT included in the repository. You MUST generate data before running the application.

### Quick Start (Recommended for Testing)

Generate a small dataset for testing (completes in ~30 seconds):

```bash
cd surfshark-vpn-analytics
python scripts/generate_vpn_data.py --servers 10 --days 7 --sessions-per-day 1000
```

**This creates:**
- 10 VPN servers
- 7 days of historical data
- ~7,000 sessions
- ~70 cost records
- Database size: ~5 MB
- **Requires: 2 GB RAM**

### Medium Dataset (Recommended for Development)

Generate a medium dataset (completes in ~2-3 minutes):

```bash
python scripts/generate_vpn_data.py --servers 50 --days 90 --sessions-per-day 10000
```

**This creates:**
- 50 VPN servers
- 90 days of historical data
- ~900,000 sessions
- ~4,500 cost records
- Database size: ~200 MB
- **Requires: 4 GB RAM**

### Full Production Dataset (Recommended for Demos)

Generate a full production dataset (completes in ~3-5 minutes):

```bash
python scripts/generate_vpn_data.py --servers 150 --days 90 --sessions-per-day 50000
```

**This creates:**
- 150 VPN servers across 5 cloud providers
- 90 days of historical data
- ~4.5 million sessions
- ~13,500 cost records
- Database size: ~1 GB
- Quarterly infrastructure cost: ~$450K
- **Requires: 6 GB RAM**

### Data Generation Command Reference

```bash
python scripts/generate_vpn_data.py [OPTIONS]
```

**Available Options:**
- `--servers N` - Number of VPN servers to create (default: 150)
- `--days N` - Number of days of historical data (default: 90)
- `--sessions-per-day N` - Average sessions per day (default: 50000)

**Examples:**

```bash
# Minimal dataset (for low-end machines)
python scripts/generate_vpn_data.py --servers 5 --days 7 --sessions-per-day 500

# Custom dataset
python scripts/generate_vpn_data.py --servers 100 --days 180 --sessions-per-day 25000
```

### Machine Requirements by Dataset Size

| Dataset | Servers | Days | Sessions/Day | RAM | Time | DB Size | Use Case |
|---------|---------|------|--------------|-----|------|---------|----------|
| **Minimal** | 5 | 7 | 500 | 1-2 GB | 15 sec | 2 MB | Quick test |
| **Small** | 10 | 7 | 1,000 | 2 GB | 30 sec | 5 MB | Testing |
| **Medium** | 50 | 90 | 10,000 | 4 GB | 2-3 min | 200 MB | Development |
| **Large** | 100 | 180 | 25,000 | 6 GB | 5 min | 800 MB | Staging |
| **Production** | 150 | 90 | 50,000 | 6 GB | 5 min | 1 GB | Demos |

### Regenerating Data

To regenerate data (this will DELETE existing data):

```bash
rm -rf surfshark-vpn-analytics/instance/
mkdir surfshark-vpn-analytics/instance
cd surfshark-vpn-analytics
python scripts/generate_vpn_data.py --servers 10 --days 7 --sessions-per-day 1000
```

## 🚀 Running the Applications

You can run **both apps simultaneously** or just one at a time. They share the same database.

### Option 1: Run Both Apps (Recommended)

**Terminal 1 - Usage Analytics Backend:**
```bash
cd surfshark-vpn-analytics
source venv/bin/activate
python cost-app/backend/app.py
```
Backend available at: **http://localhost:5002**

**Terminal 2 - Performance Analytics Backend:**
```bash
cd surfshark-vpn-analytics
source venv/bin/activate
python performance-app/backend/app.py
```
Backend available at: **http://localhost:5003**

**Terminal 3 - Usage Analytics Frontend:**
```bash
cd surfshark-vpn-analytics/cost-app/frontend
npm start
```
Frontend available at: **http://localhost:3000**

**Terminal 4 - Performance Analytics Frontend:**
```bash
cd surfshark-vpn-analytics/performance-app/frontend
npm start
```
Frontend available at: **http://localhost:3001**

### Option 2: Run Only Usage Analytics

**Terminal 1:**
```bash
cd surfshark-vpn-analytics
source venv/bin/activate
python cost-app/backend/app.py
```

**Terminal 2:**
```bash
cd surfshark-vpn-analytics/cost-app/frontend
npm start
```

Access at: **http://localhost:3000**

### Option 3: Run Only Performance Analytics

**Terminal 1:**
```bash
cd surfshark-vpn-analytics
source venv/bin/activate
python performance-app/backend/app.py
```

**Terminal 2:**
```bash
cd surfshark-vpn-analytics/performance-app/frontend
npm start
```

Access at: **http://localhost:3001**

### Access URLs

**Usage Analytics:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5002
- Health Check: http://localhost:5002/api/health

**Performance Analytics:**
- Frontend: http://localhost:3001
- Backend API: http://localhost:5003
- Health Check: http://localhost:5003/api/health

## 📁 Project Structure

```
surfshark-vpn-analytics/
├── cost-app/                    # Usage Analytics Application
│   ├── backend/
│   │   └── app.py              # Flask API (Port 5002)
│   └── frontend/               # React App (Port 3000)
│       ├── public/
│       └── src/
│           ├── api/            # API client
│           ├── components/     # React components
│           ├── pages/          # Dashboard pages
│           └── utils/          # Utility functions
├── performance-app/             # Performance Analytics Application
│   ├── backend/
│   │   └── app.py              # Flask API (Port 5003)
│   └── frontend/               # React App (Port 3001)
│       ├── public/
│       └── src/
│           ├── api/            # API client
│           ├── components/     # React components (KPICard, TrendChart, etc.)
│           ├── pages/          # Dashboard pages
│           └── utils/          # Utility functions
├── shared/                      # Shared Infrastructure
│   ├── data_layer/
│   │   ├── models.py           # SQLAlchemy models (VPNSession, VPNServer, etc.)
│   │   ├── repositories.py     # Data access layer (Cost & Performance)
│   │   └── config.py           # Database configuration
│   └── data_generators/
│       └── vpn_data_generator.py  # Data generation logic
├── scripts/
│   └── generate_vpn_data.py    # Data generation CLI
├── instance/                    # Database directory (gitignored)
│   └── surfshark_vpn.db        # Shared SQLite database
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🔌 API Endpoints

### Usage Analytics API (Port 5002)
- `GET /api/cost/executive/summary?days=30` - Executive KPIs
- `GET /api/cost/trends?days=30` - Daily cost trends
- `GET /api/cost/by-provider?days=30` - Cost by provider
- `GET /api/cost/by-location?days=30` - Cost by location
- `GET /api/cost/by-server?days=30&limit=10` - Top cost servers
- `GET /api/servers/utilization?days=30&limit=20` - Server utilization
- `GET /api/providers` - List all providers
- `GET /api/health` - Health check

### Performance Analytics API (Port 5003)
- `GET /api/performance/connectivity/summary?days=30` - Connectivity rate (PRIMARY KPI)
- `GET /api/performance/latency?days=30` - Connection latency metrics
- `GET /api/performance/quality?days=30` - Network quality metrics
- `GET /api/performance/user-satisfaction?days=30` - User rating metrics
- `GET /api/performance/trends?days=30` - Daily performance trends
- `GET /api/performance/by-protocol?days=30` - Performance by protocol
- `GET /api/performance/by-server?days=30&limit=20` - Server performance
- `GET /api/performance/by-location?days=30` - Location performance
- `GET /api/providers` - List all providers
- `GET /api/health` - Health check

## 🎨 Data Model

### Providers
- AWS, Google Cloud, Azure, DigitalOcean, Vultr
- Realistic pricing: $110-$180/month per server
- Data transfer costs: $0.01-$0.09 per GB

### VPN Servers
- 150 servers across 20+ global locations
- CPU: Intel Xeon / AMD EPYC
- RAM: 32-256 GB
- Cores: 8-64

### Sessions
- Realistic connection patterns (peak hours, weekends)
- Multiple platforms: Windows, iOS, Android, macOS, Linux
- Connection protocols: WireGuard, OpenVPN, IKEv2
- Quality metrics: reconnects, disconnects, network issues

### Costs
- Daily cost records per server
- Base infrastructure cost
- Data transfer cost
- Session and utilization metrics

## 🐛 Troubleshooting

### Database Not Found Error

```
sqlite3.OperationalError: unable to open database file
```

**Solution:** Generate data first:
```bash
mkdir surfshark-vpn-analytics/instance
cd surfshark-vpn-analytics
python scripts/generate_vpn_data.py --servers 10 --days 7 --sessions-per-day 1000
```

### Port Already in Use

**Backend (5002):**
```bash
lsof -ti:5002 | xargs kill -9
```

**Frontend (3000):**
```bash
lsof -ti:3000 | xargs kill -9
```

### Memory Issues During Data Generation

Reduce dataset size:
```bash
python scripts/generate_vpn_data.py --servers 5 --days 7 --sessions-per-day 500
```

### Probability Sum Error

If you see `probabilities do not sum to 1`, ensure you have the latest code with the normalized probability fix.

## 📝 Environment Variables

Create a `.env` file in the `surfshark-vpn-analytics` directory (or copy from `.env.example`):

```bash
# Flask Configuration
FLASK_APP=cost-app/backend/app.py
FLASK_ENV=development
FLASK_DEBUG=1

# Database (handled by config.py - no need to set)
#DATABASE_URL=sqlite:///instance/surfshark_vpn.db

# API Configuration
API_PORT=5002
PERFORMANCE_API_PORT=5003
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Data Generation Settings
GENERATE_DAYS=90
NUM_SERVERS=150
NUM_SESSIONS_PER_DAY=50000
```

**Note:** The database path is automatically configured in `shared/data_layer/config.py` and doesn't need to be set in `.env`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with Flask, React, Material-UI, and Recharts
- Inspired by real-world VPN infrastructure analytics needs
- Sample data generated using Faker and NumPy