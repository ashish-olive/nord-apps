"""Flask application for Surfshark VPN Cost Analytics"""
import sys
from pathlib import Path
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.data_layer.config import AppConfig
from shared.data_layer.models import db
from shared.data_layer.repositories import (
    ServerCostRepository, VPNSessionRepository, 
    VPNServerRepository, ProviderRepository
)
from shared.utils.helpers import get_date_range_from_params

# Create Flask app
app = Flask(__name__)
app.config.from_object(AppConfig)

# Initialize extensions
db.init_app(app)
CORS(app)

@app.route('/')
def index():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'Surfshark VPN Cost Analytics API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'executive_summary': '/api/cost/executive/summary',
            'cost_trends': '/api/cost/trends',
            'cost_by_provider': '/api/cost/by-provider',
            'cost_by_location': '/api/cost/by-location',
            'cost_by_server': '/api/cost/by-server',
            'server_utilization': '/api/servers/utilization',
            'providers': '/api/providers'
        }
    })

@app.route('/api/debug/paths')
def debug_paths():
    """Debug endpoint to show paths"""
    import os
    return jsonify({
        'database_uri': app.config['SQLALCHEMY_DATABASE_URI'],
        'db_path': getattr(AppConfig, 'DB_PATH', 'NOT SET'),
        'base_dir': str(AppConfig.BASE_DIR),
        'base_dir_absolute': str(AppConfig.BASE_DIR.absolute()),
        'project_root': str(project_root),
        'current_dir': os.getcwd(),
        'app_file': str(Path(__file__)),
        'database_exists': os.path.exists(str(AppConfig.BASE_DIR / 'instance' / 'surfshark_vpn.db'))
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/cost/executive/summary')
def executive_summary():
    """Executive cost summary with KPIs"""
    from flask import request
    
    # Get date range
    days = request.args.get('days', default=30, type=int)
    start_date, end_date = get_date_range_from_params(days=days)
    
    # Get cost data
    cost_data = ServerCostRepository.get_total_cost(start_date, end_date)
    
    # Get previous period for comparison
    prev_start = start_date - timedelta(days=days)
    prev_end = start_date
    prev_cost_data = ServerCostRepository.get_total_cost(prev_start, prev_end)
    
    # Calculate changes
    total_cost_change = ((cost_data['total_cost'] - prev_cost_data['total_cost']) / 
                        prev_cost_data['total_cost'] * 100) if prev_cost_data['total_cost'] > 0 else 0
    
    cost_per_session_change = ((cost_data['cost_per_session'] - prev_cost_data['cost_per_session']) / 
                               prev_cost_data['cost_per_session'] * 100) if prev_cost_data['cost_per_session'] > 0 else 0
    
    return jsonify({
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'days': days
        },
        'metrics': {
            'total_cost': {
                'value': round(cost_data['total_cost'], 2),
                'change_percent': round(total_cost_change, 2)
            },
            'base_cost': {
                'value': round(cost_data['base_cost'], 2)
            },
            'transfer_cost': {
                'value': round(cost_data['transfer_cost'], 2)
            },
            'cost_per_session': {
                'value': round(cost_data['cost_per_session'], 4),
                'change_percent': round(cost_per_session_change, 2)
            },
            'cost_per_hour': {
                'value': round(cost_data['cost_per_hour'], 4)
            },
            'total_sessions': cost_data['total_sessions'],
            'total_hours': round(cost_data['total_hours'], 2)
        }
    })

@app.route('/api/cost/trends')
def cost_trends():
    """Get cost trends over time"""
    from flask import request
    
    days = request.args.get('days', default=30, type=int)
    start_date, end_date = get_date_range_from_params(days=days)
    
    trends = ServerCostRepository.get_cost_trend(start_date, end_date)
    
    return jsonify({
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        },
        'trends': trends
    })

@app.route('/api/cost/by-provider')
def cost_by_provider():
    """Get cost breakdown by provider"""
    from flask import request
    
    days = request.args.get('days', default=30, type=int)
    start_date, end_date = get_date_range_from_params(days=days)
    
    provider_costs = ServerCostRepository.get_cost_by_provider(start_date, end_date)
    
    return jsonify({
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        },
        'providers': provider_costs
    })

@app.route('/api/cost/by-location')
def cost_by_location():
    """Get cost breakdown by geographic location"""
    from flask import request
    
    days = request.args.get('days', default=30, type=int)
    start_date, end_date = get_date_range_from_params(days=days)
    
    location_costs = ServerCostRepository.get_cost_by_location(start_date, end_date)
    
    return jsonify({
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        },
        'locations': location_costs
    })

@app.route('/api/cost/by-server')
def cost_by_server():
    """Get top cost servers"""
    from flask import request
    
    days = request.args.get('days', default=30, type=int)
    limit = request.args.get('limit', default=10, type=int)
    start_date, end_date = get_date_range_from_params(days=days)
    
    top_servers = ServerCostRepository.get_top_cost_servers(start_date, end_date, limit=limit)
    
    return jsonify({
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        },
        'servers': top_servers
    })

@app.route('/api/servers/utilization')
def server_utilization():
    """Get server utilization metrics"""
    from flask import request
    
    days = request.args.get('days', default=30, type=int)
    limit = request.args.get('limit', default=20, type=int)
    start_date, end_date = get_date_range_from_params(days=days)
    
    utilization = VPNServerRepository.get_server_utilization(start_date, end_date, limit=limit)
    
    return jsonify({
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        },
        'servers': utilization
    })

@app.route('/api/providers')
def get_providers():
    """Get all providers"""
    providers = ProviderRepository.get_all_providers()
    
    return jsonify({
        'providers': [
            {
                'id': p.id,
                'name': p.name,
                'cost_per_server_monthly': p.cost_per_server_monthly,
                'cost_per_gb_transfer': p.cost_per_gb_transfer
            }
            for p in providers
        ]
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = AppConfig.API_PORT
    print(f"\n🚀 Starting Surfshark VPN Cost Analytics API on port {port}...")
    print(f"📊 API Documentation: http://localhost:{port}/")
    print(f"🏥 Health Check: http://localhost:{port}/api/health\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=AppConfig.DEBUG
    )