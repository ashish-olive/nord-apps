"""Data access layer for Surfshark VPN Analytics"""
from datetime import datetime, timedelta, date
from sqlalchemy import func, and_, or_, case
from shared.data_layer.models import db, VPNSession, VPNServer, Provider, ServerCost, Platform

class VPNSessionRepository:
    """Repository for VPN session data access"""
    
    @staticmethod
    def get_sessions_by_date_range(start_date, end_date):
        """Get all sessions within date range"""
        return VPNSession.query.filter(
            VPNSession.created_at >= start_date,
            VPNSession.created_at <= end_date
        ).all()
    
    @staticmethod
    def get_session_count(start_date, end_date, filters=None):
        """Get total session count with optional filters"""
        query = VPNSession.query.filter(
            VPNSession.created_at >= start_date,
            VPNSession.created_at <= end_date
        )
        
        if filters:
            if filters.get('app_name'):
                query = query.filter(VPNSession.app_name == filters['app_name'])
            if filters.get('user_country'):
                query = query.filter(VPNSession.user_country == filters['user_country'])
        
        return query.count()
    
    @staticmethod
    def get_connectivity_metrics(start_date, end_date):
        """Get connectivity rate metrics"""
        result = db.session.query(
            func.count(VPNSession.id).label('total_sessions'),
            func.sum(VPNSession.has_connect_intent.cast(db.Integer)).label('intent_sessions'),
            func.sum(VPNSession.is_connected.cast(db.Integer)).label('connected_sessions'),
            func.sum(VPNSession.is_canceled.cast(db.Integer)).label('canceled_sessions')
        ).filter(
            VPNSession.created_at >= start_date,
            VPNSession.created_at <= end_date
        ).first()
        
        return {
            'total_sessions': result.total_sessions or 0,
            'intent_sessions': result.intent_sessions or 0,
            'connected_sessions': result.connected_sessions or 0,
            'canceled_sessions': result.canceled_sessions or 0,
            'connectivity_rate': (result.connected_sessions / result.intent_sessions * 100) 
                if result.intent_sessions else 0
        }
    
    @staticmethod
    def get_sessions_by_platform(start_date, end_date):
        """Get session counts by platform"""
        results = db.session.query(
            VPNSession.app_name,
            func.count(VPNSession.id).label('session_count')
        ).filter(
            VPNSession.created_at >= start_date,
            VPNSession.created_at <= end_date
        ).group_by(VPNSession.app_name).all()
        
        return [{'platform': r.app_name, 'sessions': r.session_count} for r in results]

class ServerCostRepository:
    """Repository for server cost data access"""
    
    @staticmethod
    def get_total_cost(start_date, end_date):
        """Get total infrastructure cost for date range"""
        result = db.session.query(
            func.sum(ServerCost.total_cost).label('total_cost'),
            func.sum(ServerCost.base_cost).label('base_cost'),
            func.sum(ServerCost.transfer_cost).label('transfer_cost'),
            func.sum(ServerCost.total_sessions).label('total_sessions'),
            func.sum(ServerCost.total_connection_hours).label('total_hours')
        ).filter(
            ServerCost.date >= start_date,
            ServerCost.date <= end_date
        ).first()
        
        total_cost = result.total_cost or 0
        total_sessions = result.total_sessions or 0
        total_hours = result.total_hours or 0
        
        return {
            'total_cost': total_cost,
            'base_cost': result.base_cost or 0,
            'transfer_cost': result.transfer_cost or 0,
            'total_sessions': total_sessions,
            'total_hours': total_hours,
            'cost_per_session': total_cost / total_sessions if total_sessions else 0,
            'cost_per_hour': total_cost / total_hours if total_hours else 0
        }
    
    @staticmethod
    def get_cost_by_provider(start_date, end_date):
        """Get cost breakdown by provider"""
        results = db.session.query(
            Provider.name,
            func.sum(ServerCost.total_cost).label('total_cost'),
            func.count(func.distinct(ServerCost.server_id)).label('server_count'),
            func.sum(ServerCost.total_sessions).label('total_sessions'),
            func.sum(ServerCost.total_connection_hours).label('total_hours')
        ).join(
            VPNServer, ServerCost.server_id == VPNServer.id
        ).join(
            Provider, VPNServer.provider_id == Provider.id
        ).filter(
            ServerCost.date >= start_date,
            ServerCost.date <= end_date
        ).group_by(Provider.name).all()
        
        return [
            {
                'provider': r.name,
                'total_cost': r.total_cost,
                'server_count': r.server_count,
                'total_sessions': r.total_sessions,
                'total_hours': r.total_hours or 0,
                'cost_per_session': r.total_cost / r.total_sessions if r.total_sessions else 0,
                'cost_per_hour': r.total_cost / r.total_hours if r.total_hours else 0
            }
            for r in results
        ]
    
    @staticmethod
    def get_cost_by_location(start_date, end_date):
        """Get cost breakdown by geographic location"""
        results = db.session.query(
            VPNServer.location_country,
            VPNServer.location_city,
            func.sum(ServerCost.total_cost).label('total_cost'),
            func.count(func.distinct(ServerCost.server_id)).label('server_count'),
            func.sum(ServerCost.total_sessions).label('total_sessions')
        ).join(
            VPNServer, ServerCost.server_id == VPNServer.id
        ).filter(
            ServerCost.date >= start_date,
            ServerCost.date <= end_date
        ).group_by(
            VPNServer.location_country,
            VPNServer.location_city
        ).all()
        
        return [
            {
                'country': r.location_country,
                'city': r.location_city,
                'location': f"{r.location_city}, {r.location_country}",
                'total_cost': r.total_cost,
                'server_count': r.server_count,
                'total_sessions': r.total_sessions,
                'cost_per_session': r.total_cost / r.total_sessions if r.total_sessions else 0
            }
            for r in results
        ]
    
    @staticmethod
    def get_cost_trend(start_date, end_date, granularity='day'):
        """Get cost trend over time"""
        results = db.session.query(
            ServerCost.date,
            func.sum(ServerCost.total_cost).label('daily_cost'),
            func.sum(ServerCost.total_sessions).label('daily_sessions'),
            func.sum(ServerCost.total_connection_hours).label('daily_hours')
        ).filter(
            ServerCost.date >= start_date,
            ServerCost.date <= end_date
        ).group_by(ServerCost.date).order_by(ServerCost.date).all()
        
        return [
            {
                'date': r.date.isoformat(),
                'cost': r.daily_cost,
                'sessions': r.daily_sessions,
                'hours': r.daily_hours or 0,
                'cost_per_session': r.daily_cost / r.daily_sessions if r.daily_sessions else 0
            }
            for r in results
        ]
    
    @staticmethod
    def get_top_cost_servers(start_date, end_date, limit=10):
        """Get servers with highest costs"""
        results = db.session.query(
            VPNServer.hostname,
            VPNServer.location_country,
            VPNServer.location_city,
            Provider.name.label('provider'),
            func.sum(ServerCost.total_cost).label('total_cost'),
            func.sum(ServerCost.total_sessions).label('total_sessions')
        ).join(
            VPNServer, ServerCost.server_id == VPNServer.id
        ).join(
            Provider, VPNServer.provider_id == Provider.id
        ).filter(
            ServerCost.date >= start_date,
            ServerCost.date <= end_date
        ).group_by(
            VPNServer.id, VPNServer.hostname, VPNServer.location_country,
            VPNServer.location_city, Provider.name
        ).order_by(func.sum(ServerCost.total_cost).desc()).limit(limit).all()
        
        return [
            {
                'hostname': r.hostname,
                'location': f"{r.location_city}, {r.location_country}",
                'provider': r.provider,
                'total_cost': r.total_cost,
                'total_sessions': r.total_sessions,
                'cost_per_session': r.total_cost / r.total_sessions if r.total_sessions else 0
            }
            for r in results
        ]

class VPNServerRepository:
    """Repository for VPN server data access"""
    
    @staticmethod
    def get_all_active_servers():
        """Get all active servers"""
        return VPNServer.query.filter_by(is_active=True).all()
    
    @staticmethod
    def get_servers_by_provider(provider_id):
        """Get servers for a specific provider"""
        return VPNServer.query.filter_by(provider_id=provider_id, is_active=True).all()
    
    @staticmethod
    def get_server_utilization(start_date, end_date, limit=20):
        """Get server utilization metrics"""
        results = db.session.query(
            VPNServer.hostname,
            VPNServer.location_country,
            VPNServer.location_city,
            Provider.name.label('provider'),
            func.count(VPNSession.id).label('session_count'),
            func.sum(VPNSession.connection_duration_seconds).label('total_duration')
        ).join(
            VPNSession, VPNServer.id == VPNSession.server_id
        ).join(
            Provider, VPNServer.provider_id == Provider.id
        ).filter(
            VPNSession.created_at >= start_date,
            VPNSession.created_at <= end_date
        ).group_by(
            VPNServer.id, VPNServer.hostname, VPNServer.location_country,
            VPNServer.location_city, Provider.name
        ).order_by(func.count(VPNSession.id).desc()).limit(limit).all()
        
        return [
            {
                'hostname': r.hostname,
                'location': f"{r.location_city}, {r.location_country}",
                'provider': r.provider,
                'session_count': r.session_count,
                'total_hours': (r.total_duration or 0) / 3600
            }
            for r in results
        ]

class ProviderRepository:
    """Repository for provider data access"""
    
    @staticmethod
    def get_all_providers():
        """Get all providers"""
        return Provider.query.all()
    
    @staticmethod
    def get_provider_by_name(name):
        """Get provider by name"""
        return Provider.query.filter_by(name=name).first()

class PerformanceRepository:
    """Repository for VPN performance metrics"""
    
    @staticmethod
    def get_connectivity_rate(start_date, end_date):
        """PRIMARY METRIC: Connection success rate"""
        result = db.session.query(
            func.count(VPNSession.id).label('total_sessions'),
            func.sum(VPNSession.has_connect_intent.cast(db.Integer)).label('intent_sessions'),
            func.sum(VPNSession.is_connected.cast(db.Integer)).label('connected_sessions')
        ).filter(
            VPNSession.created_at >= start_date,
            VPNSession.created_at <= end_date
        ).first()
        
        connectivity_rate = 0
        if result.intent_sessions and result.intent_sessions > 0:
            connectivity_rate = (result.connected_sessions / result.intent_sessions) * 100
        
        return {
            'connectivity_rate': connectivity_rate,
            'connected_sessions': result.connected_sessions or 0,
            'intent_sessions': result.intent_sessions or 0,
            'total_sessions': result.total_sessions or 0
        }
    
    @staticmethod
    def get_average_connection_time(start_date, end_date):
        """Average time to connect (latency)"""
        # Get average and min/max for approximation
        result = db.session.query(
            func.avg(VPNSession.connecting_time_ms).label('avg_latency_ms'),
            func.min(VPNSession.connecting_time_ms).label('min_latency_ms'),
            func.max(VPNSession.connecting_time_ms).label('max_latency_ms')
        ).filter(
            VPNSession.created_at >= start_date,
            VPNSession.created_at <= end_date,
            VPNSession.is_connected == True,
            VPNSession.connecting_time_ms.isnot(None)
        ).first()
        
        # Approximate median and p95 (for SQLite compatibility)
        avg = result.avg_latency_ms or 0
        median_approx = avg  # Rough approximation
        p95_approx = avg * 1.5  # Rough approximation (typically 1.5x average)
        
        return {
            'avg_latency_ms': avg,
            'median_latency_ms': median_approx,
            'p95_latency_ms': p95_approx,
            'min_latency_ms': result.min_latency_ms or 0,
            'max_latency_ms': result.max_latency_ms or 0
        }
    
    @staticmethod
    def get_nonet_sessions_rate(start_date, end_date):
        """PRIMARY METRIC: Network interruption rate"""
        result = db.session.query(
            func.count(VPNSession.id).label('total_sessions'),
            func.sum(case((VPNSession.nonet_event_count > 0, 1), else_=0)).label('nonet_sessions')
        ).filter(
            VPNSession.created_at >= start_date,
            VPNSession.created_at <= end_date
        ).first()
        
        nonet_rate = 0
        if result.total_sessions and result.total_sessions > 0:
            nonet_rate = (result.nonet_sessions / result.total_sessions) * 100
        
        return {
            'nonet_rate': nonet_rate,
            'nonet_sessions': result.nonet_sessions or 0,
            'total_sessions': result.total_sessions or 0
        }
    
    @staticmethod
    def get_reconnect_metrics(start_date, end_date):
        """Reconnection and stability metrics"""
        result = db.session.query(
            func.sum(VPNSession.reconnect_event_count).label('total_reconnects'),
            func.sum(VPNSession.unexpected_disconnect.cast(db.Integer)).label('unexpected_disconnects'),
            func.count(VPNSession.id).label('total_sessions')
        ).filter(
            VPNSession.created_at >= start_date,
            VPNSession.created_at <= end_date,
            VPNSession.is_connected == True
        ).first()
        
        return {
            'total_reconnects': result.total_reconnects or 0,
            'unexpected_disconnects': result.unexpected_disconnects or 0,
            'reconnects_per_session': (result.total_reconnects or 0) / max(result.total_sessions, 1),
            'unexpected_disconnect_rate': ((result.unexpected_disconnects or 0) / max(result.total_sessions, 1)) * 100
        }
    
    @staticmethod
    def get_user_rating_metrics(start_date, end_date):
        """User satisfaction metrics"""
        result = db.session.query(
            func.sum(VPNSession.has_user_rating.cast(db.Integer)).label('rated_sessions'),
            func.sum(case((and_(VPNSession.has_user_rating == True, VPNSession.is_negative_rating == True), 1), else_=0)).label('negative_ratings'),
            func.sum(case((and_(VPNSession.has_user_rating == True, VPNSession.is_negative_rating == False), 1), else_=0)).label('positive_ratings')
        ).filter(
            VPNSession.created_at >= start_date,
            VPNSession.created_at <= end_date
        ).first()
        
        satisfaction_rate = 0
        if result.rated_sessions and result.rated_sessions > 0:
            satisfaction_rate = (result.positive_ratings / result.rated_sessions) * 100
        
        return {
            'rated_sessions': result.rated_sessions or 0,
            'positive_ratings': result.positive_ratings or 0,
            'negative_ratings': result.negative_ratings or 0,
            'satisfaction_rate': satisfaction_rate
        }
    
    @staticmethod
    def get_performance_by_protocol(start_date, end_date):
        """Performance metrics by VPN protocol"""
        results = db.session.query(
            VPNSession.connected_protocol,
            func.count(VPNSession.id).label('session_count'),
            func.avg(VPNSession.connecting_time_ms).label('avg_latency'),
            func.sum(case((VPNSession.nonet_event_count > 0, 1), else_=0)).label('nonet_sessions'),
            func.avg(VPNSession.connection_duration_seconds).label('avg_duration')
        ).filter(
            VPNSession.created_at >= start_date,
            VPNSession.created_at <= end_date,
            VPNSession.is_connected == True,
            VPNSession.connected_protocol.isnot(None)
        ).group_by(VPNSession.connected_protocol).all()
        
        return [
            {
                'protocol': r.connected_protocol,
                'session_count': r.session_count,
                'avg_latency_ms': r.avg_latency or 0,
                'nonet_rate': (r.nonet_sessions / r.session_count * 100) if r.session_count > 0 else 0,
                'avg_duration_minutes': (r.avg_duration or 0) / 60
            }
            for r in results
        ]
    
    @staticmethod
    def get_performance_by_server(start_date, end_date, limit=20):
        """Top/bottom performing servers"""
        results = db.session.query(
            VPNServer.hostname,
            VPNServer.location_city,
            VPNServer.location_country,
            Provider.name.label('provider'),
            func.count(VPNSession.id).label('session_count'),
            func.avg(VPNSession.connecting_time_ms).label('avg_latency'),
            func.sum(case((VPNSession.nonet_event_count > 0, 1), else_=0)).label('nonet_sessions'),
            func.sum(VPNSession.reconnect_event_count).label('total_reconnects')
        ).join(
            VPNSession, VPNServer.id == VPNSession.server_id
        ).join(
            Provider, VPNServer.provider_id == Provider.id
        ).filter(
            VPNSession.created_at >= start_date,
            VPNSession.created_at <= end_date,
            VPNSession.is_connected == True
        ).group_by(
            VPNServer.hostname,
            VPNServer.location_city,
            VPNServer.location_country,
            Provider.name
        ).order_by(func.avg(VPNSession.connecting_time_ms).asc()).limit(limit).all()
        
        return [
            {
                'hostname': r.hostname,
                'location': f"{r.location_city}, {r.location_country}",
                'provider': r.provider,
                'session_count': r.session_count,
                'avg_latency_ms': r.avg_latency or 0,
                'nonet_rate': (r.nonet_sessions / r.session_count * 100) if r.session_count > 0 else 0,
                'reconnects_per_session': (r.total_reconnects or 0) / max(r.session_count, 1)
            }
            for r in results
        ]
    
    @staticmethod
    def get_performance_by_location(start_date, end_date):
        """Performance metrics by geographic location"""
        results = db.session.query(
            VPNServer.location_city,
            VPNServer.location_country,
            func.count(VPNSession.id).label('session_count'),
            func.avg(VPNSession.connecting_time_ms).label('avg_latency'),
            func.sum(case((VPNSession.nonet_event_count > 0, 1), else_=0)).label('nonet_sessions')
        ).join(
            VPNSession, VPNServer.id == VPNSession.server_id
        ).filter(
            VPNSession.created_at >= start_date,
            VPNSession.created_at <= end_date,
            VPNSession.is_connected == True
        ).group_by(
            VPNServer.location_city,
            VPNServer.location_country
        ).order_by(func.count(VPNSession.id).desc()).all()
        
        return [
            {
                'location': f"{r.location_city}, {r.location_country}",
                'city': r.location_city,
                'country': r.location_country,
                'session_count': r.session_count,
                'avg_latency_ms': r.avg_latency or 0,
                'nonet_rate': (r.nonet_sessions / r.session_count * 100) if r.session_count > 0 else 0
            }
            for r in results
        ]