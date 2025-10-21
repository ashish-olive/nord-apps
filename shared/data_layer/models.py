"""SQLAlchemy models for Surfshark VPN Analytics"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Index

db = SQLAlchemy()

class Provider(db.Model):
    """Hosting provider information"""
    __tablename__ = 'providers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    cost_per_server_monthly = db.Column(db.Float, nullable=False)
    cost_per_gb_transfer = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    servers = db.relationship('VPNServer', backref='provider', lazy='dynamic')

class VPNServer(db.Model):
    """VPN server infrastructure"""
    __tablename__ = 'vpn_servers'
    
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(200), nullable=False, unique=True)
    ip_address = db.Column(db.String(45), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=False)
    location_country = db.Column(db.String(100), nullable=False)
    location_city = db.Column(db.String(100), nullable=False)
    cpu_model = db.Column(db.String(200))
    cpu_cores = db.Column(db.Integer)
    ram_gb = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sessions = db.relationship('VPNSession', backref='server', lazy='dynamic')
    cost_records = db.relationship('ServerCost', backref='server', lazy='dynamic')
    
    # Indexes
    __table_args__ = (
        Index('idx_server_location', 'location_country', 'location_city'),
        Index('idx_server_provider', 'provider_id'),
    )

class VPNSession(db.Model):
    """VPN session data"""
    __tablename__ = 'vpn_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, unique=True)
    server_id = db.Column(db.Integer, db.ForeignKey('vpn_servers.id'), nullable=False)
    
    # Session metadata
    app_name = db.Column(db.String(50), nullable=False)
    app_version = db.Column(db.String(50))
    device_model = db.Column(db.String(100))
    user_country = db.Column(db.String(100), nullable=False)
    
    # Timing
    created_at = db.Column(db.DateTime, nullable=False)
    connect_intent_at = db.Column(db.DateTime)
    connected_at = db.Column(db.DateTime)
    disconnected_at = db.Column(db.DateTime)
    canceled_at = db.Column(db.DateTime)
    
    # Connection details
    connected_protocol = db.Column(db.String(50))
    connection_duration_seconds = db.Column(db.Integer, default=0)
    
    # Performance metrics - Connection intent and latency
    connect_intent_trigger = db.Column(db.String(100))  # 'user_action', 'auto_connect', 'quick_connect'
    connecting_time_ms = db.Column(db.Integer)  # Time from intent to connected (latency)
    
    # Performance metrics - Disconnect tracking
    disconnect_intent_at = db.Column(db.DateTime)
    disconnect_intent_trigger = db.Column(db.String(100))  # 'user_action', 'app_close', 'switch_server'
    
    # Quality metrics
    has_connect_intent = db.Column(db.Boolean, default=False)
    is_connected = db.Column(db.Boolean, default=False)
    is_canceled = db.Column(db.Boolean, default=False)
    nonet_event_count = db.Column(db.Integer, default=0)
    nonet_total_duration_ms = db.Column(db.Integer, default=0)
    reconnect_event_count = db.Column(db.Integer, default=0)
    unexpected_disconnect = db.Column(db.Boolean, default=False)
    
    # User feedback
    has_user_rating = db.Column(db.Boolean, default=False)
    is_negative_rating = db.Column(db.Boolean, default=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_session_created', 'created_at'),
        Index('idx_session_server', 'server_id'),
        Index('idx_session_country', 'user_country'),
        Index('idx_session_app', 'app_name'),
    )

class ServerCost(db.Model):
    """Daily cost records per server"""
    __tablename__ = 'server_costs'
    
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('vpn_servers.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    # Cost breakdown
    base_cost = db.Column(db.Float, nullable=False)  # Daily server cost
    transfer_cost = db.Column(db.Float, default=0.0)  # Data transfer cost
    total_cost = db.Column(db.Float, nullable=False)
    
    # Usage metrics
    total_sessions = db.Column(db.Integer, default=0)
    total_connection_hours = db.Column(db.Float, default=0.0)
    total_gb_transferred = db.Column(db.Float, default=0.0)
    
    # Indexes
    __table_args__ = (
        Index('idx_cost_date', 'date'),
        Index('idx_cost_server_date', 'server_id', 'date'),
    )

class Platform(db.Model):
    """Platform/app information"""
    __tablename__ = 'platforms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    display_name = db.Column(db.String(100), nullable=False)
    is_mobile = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)