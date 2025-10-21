#!/usr/bin/env python3
"""
Surfshark VPN Performance Analytics API
Provides performance metrics, connectivity rates, and quality monitoring
"""
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.data_layer.config import AppConfig
from shared.data_layer.models import db
from shared.data_layer.repositories import PerformanceRepository, ProviderRepository

# Create Flask app
app = Flask(__name__)
app.config.from_object(AppConfig)

# Initialize database
db.init_app(app)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": AppConfig.CORS_ORIGINS}})

# Helper function to parse date range
def get_date_range(days=30):
    """Get date range for queries"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

@app.route('/')
def index():
    """API documentation"""
    return jsonify({
        'name': 'Surfshark VPN Performance Analytics API',
        'version': '1.0.0',
        'description': 'Performance monitoring and quality metrics for VPN infrastructure',
        'endpoints': {
            'health': '/api/health',
            'connectivity_summary': '/api/performance/connectivity/summary',
            'latency_metrics': '/api/performance/latency',
            'quality_metrics': '/api/performance/quality',
            'protocol_performance': '/api/performance/by-protocol',
            'server_performance': '/api/performance/by-server',
            'location_performance': '/api/performance/by-location',
            'user_satisfaction': '/api/performance/user-satisfaction'
        }
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'performance-analytics',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/performance/connectivity/summary')
def connectivity_summary():
    """
    PRIMARY METRIC: Connectivity rate and connection success metrics
    Query params: days (default: 30)
    """
    try:
        days = int(request.args.get('days', 30))
        start_date, end_date = get_date_range(days)
        
        # Get connectivity metrics
        connectivity = PerformanceRepository.get_connectivity_rate(start_date, end_date)
        
        return jsonify({
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days': days
            },
            'metrics': {
                'connectivity_rate': {
                    'value': round(connectivity['connectivity_rate'], 2),
                    'unit': 'percent',
                    'description': 'Percentage of successful connections out of connection attempts'
                },
                'connected_sessions': connectivity['connected_sessions'],
                'intent_sessions': connectivity['intent_sessions'],
                'total_sessions': connectivity['total_sessions'],
                'failed_connections': connectivity['intent_sessions'] - connectivity['connected_sessions']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance/latency')
def latency_metrics():
    """
    Connection latency metrics (time to connect)
    Query params: days (default: 30)
    """
    try:
        days = int(request.args.get('days', 30))
        start_date, end_date = get_date_range(days)
        
        latency = PerformanceRepository.get_average_connection_time(start_date, end_date)
        
        return jsonify({
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days': days
            },
            'metrics': {
                'average_latency_ms': round(latency['avg_latency_ms'], 0),
                'median_latency_ms': round(latency['median_latency_ms'], 0),
                'p95_latency_ms': round(latency['p95_latency_ms'], 0),
                'average_latency_seconds': round(latency['avg_latency_ms'] / 1000, 2)
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance/quality')
def quality_metrics():
    """
    Network quality metrics: nonet rate, reconnects, unexpected disconnects
    Query params: days (default: 30)
    """
    try:
        days = int(request.args.get('days', 30))
        start_date, end_date = get_date_range(days)
        
        # Get quality metrics
        nonet = PerformanceRepository.get_nonet_sessions_rate(start_date, end_date)
        reconnects = PerformanceRepository.get_reconnect_metrics(start_date, end_date)
        
        return jsonify({
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days': days
            },
            'metrics': {
                'nonet_rate': {
                    'value': round(nonet['nonet_rate'], 2),
                    'unit': 'percent',
                    'description': 'Percentage of sessions with network interruptions'
                },
                'nonet_sessions': nonet['nonet_sessions'],
                'total_reconnects': reconnects['total_reconnects'],
                'reconnects_per_session': round(reconnects['reconnects_per_session'], 3),
                'unexpected_disconnects': reconnects['unexpected_disconnects'],
                'unexpected_disconnect_rate': round(reconnects['unexpected_disconnect_rate'], 2)
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance/by-protocol')
def performance_by_protocol():
    """
    Performance comparison by VPN protocol
    Query params: days (default: 30)
    """
    try:
        days = int(request.args.get('days', 30))
        start_date, end_date = get_date_range(days)
        
        protocols = PerformanceRepository.get_performance_by_protocol(start_date, end_date)
        
        return jsonify({
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days': days
            },
            'protocols': [
                {
                    'protocol': p['protocol'],
                    'session_count': p['session_count'],
                    'avg_latency_ms': round(p['avg_latency_ms'], 0),
                    'nonet_rate': round(p['nonet_rate'], 2),
                    'avg_duration_minutes': round(p['avg_duration_minutes'], 1)
                }
                for p in protocols
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance/by-server')
def performance_by_server():
    """
    Performance metrics by VPN server
    Query params: days (default: 30), limit (default: 20)
    """
    try:
        days = int(request.args.get('days', 30))
        limit = int(request.args.get('limit', 20))
        start_date, end_date = get_date_range(days)
        
        servers = PerformanceRepository.get_performance_by_server(start_date, end_date, limit)
        
        return jsonify({
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days': days
            },
            'servers': [
                {
                    'hostname': s['hostname'],
                    'location': s['location'],
                    'provider': s['provider'],
                    'session_count': s['session_count'],
                    'avg_latency_ms': round(s['avg_latency_ms'], 0),
                    'nonet_rate': round(s['nonet_rate'], 2),
                    'reconnects_per_session': round(s['reconnects_per_session'], 3)
                }
                for s in servers
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance/by-location')
def performance_by_location():
    """
    Performance metrics by geographic location
    Query params: days (default: 30)
    """
    try:
        days = int(request.args.get('days', 30))
        start_date, end_date = get_date_range(days)
        
        locations = PerformanceRepository.get_performance_by_location(start_date, end_date)
        
        return jsonify({
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days': days
            },
            'locations': [
                {
                    'location': loc['location'],
                    'city': loc['city'],
                    'country': loc['country'],
                    'session_count': loc['session_count'],
                    'avg_latency_ms': round(loc['avg_latency_ms'], 0),
                    'nonet_rate': round(loc['nonet_rate'], 2)
                }
                for loc in locations
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance/user-satisfaction')
def user_satisfaction():
    """
    User satisfaction metrics from session ratings
    Query params: days (default: 30)
    """
    try:
        days = int(request.args.get('days', 30))
        start_date, end_date = get_date_range(days)
        
        ratings = PerformanceRepository.get_user_rating_metrics(start_date, end_date)
        
        return jsonify({
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days': days
            },
            'metrics': {
                'satisfaction_rate': {
                    'value': round(ratings['satisfaction_rate'], 2),
                    'unit': 'percent',
                    'description': 'Percentage of positive ratings out of all ratings'
                },
                'rated_sessions': ratings['rated_sessions'],
                'positive_ratings': ratings['positive_ratings'],
                'negative_ratings': ratings['negative_ratings']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance/trends')
def performance_trends():
    """
    Daily performance trends over time
    Query params: days (default: 30)
    """
    try:
        days = int(request.args.get('days', 30))
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get daily metrics
        from shared.data_layer.models import db, VPNSession
        from sqlalchemy import func
        
        daily_metrics = db.session.query(
            func.date(VPNSession.created_at).label('date'),
            func.count(VPNSession.id).label('total_sessions'),
            func.sum(VPNSession.has_connect_intent.cast(db.Integer)).label('intent_sessions'),
            func.sum(VPNSession.is_connected.cast(db.Integer)).label('connected_sessions'),
            func.avg(VPNSession.connecting_time_ms).label('avg_latency')
        ).filter(
            VPNSession.created_at >= start_date,
            VPNSession.created_at <= end_date
        ).group_by(
            func.date(VPNSession.created_at)
        ).order_by('date').all()
        
        trends = []
        for metric in daily_metrics:
            connectivity_rate = 0
            if metric.intent_sessions and metric.intent_sessions > 0:
                connectivity_rate = (metric.connected_sessions / metric.intent_sessions) * 100
            
            trends.append({
                'date': metric.date,  # Already a string from func.date()
                'connectivity_rate': round(connectivity_rate, 2),
                'avg_latency_ms': round(metric.avg_latency or 0, 0),
                'total_sessions': metric.total_sessions
            })
        
        return jsonify({
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days': days
            },
            'trends': trends
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/providers')
def get_providers():
    """Get all cloud providers"""
    try:
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PERFORMANCE_API_PORT', 5003))
    print(f"\n🚀 Starting Surfshark VPN Performance Analytics API on port {port}...")
    print(f"📊 API Documentation: http://localhost:{port}/")
    print(f"🏥 Health Check: http://localhost:{port}/api/health\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=AppConfig.DEBUG
    )
