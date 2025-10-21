"""VPN Data Generator for Surfshark Analytics"""
import random
import uuid
from datetime import datetime, timedelta, date
from faker import Faker
import numpy as np

fake = Faker()

class VPNDataGenerator:
    """Generate realistic VPN session and infrastructure data"""
    
    # Platform definitions
    PLATFORMS = [
        {'name': 'windows', 'display_name': 'Windows', 'is_mobile': False, 'weight': 0.25},
        {'name': 'ios', 'display_name': 'iOS', 'is_mobile': True, 'weight': 0.20},
        {'name': 'android', 'display_name': 'Android', 'is_mobile': True, 'weight': 0.25},
        {'name': 'macos', 'display_name': 'macOS', 'is_mobile': False, 'weight': 0.15},
        {'name': 'linux', 'display_name': 'Linux', 'is_mobile': False, 'weight': 0.08},
        {'name': 'browser_extension', 'display_name': 'Browser Extension', 'is_mobile': False, 'weight': 0.05},
        {'name': 'amazon_firestick', 'display_name': 'Amazon FireStick', 'is_mobile': False, 'weight': 0.02},
    ]
    
    # Provider definitions with realistic pricing
    PROVIDERS = [
        {'name': 'AWS', 'cost_per_server_monthly': 180.0, 'cost_per_gb_transfer': 0.09},
        {'name': 'Google Cloud', 'cost_per_server_monthly': 165.0, 'cost_per_gb_transfer': 0.08},
        {'name': 'Azure', 'cost_per_server_monthly': 175.0, 'cost_per_gb_transfer': 0.087},
        {'name': 'DigitalOcean', 'cost_per_server_monthly': 120.0, 'cost_per_gb_transfer': 0.01},
        {'name': 'Vultr', 'cost_per_server_monthly': 110.0, 'cost_per_gb_transfer': 0.01},
    ]
    
    # VPN server locations (city, country)
    LOCATIONS = [
        ('London', 'United Kingdom'), ('Manchester', 'United Kingdom'),
        ('New York', 'United States'), ('Los Angeles', 'United States'), ('Chicago', 'United States'),
        ('Toronto', 'Canada'), ('Vancouver', 'Canada'),
        ('Frankfurt', 'Germany'), ('Berlin', 'Germany'),
        ('Paris', 'France'), ('Amsterdam', 'Netherlands'),
        ('Singapore', 'Singapore'), ('Tokyo', 'Japan'), ('Sydney', 'Australia'),
        ('Mumbai', 'India'), ('Bangalore', 'India'),
        ('São Paulo', 'Brazil'), ('Stockholm', 'Sweden'),
        ('Warsaw', 'Poland'), ('Madrid', 'Spain'),
    ]
    
    # User countries (where users connect from)
    USER_COUNTRIES = [
        'United States', 'United Kingdom', 'Germany', 'France', 'Canada',
        'Australia', 'India', 'Brazil', 'Japan', 'Spain', 'Italy',
        'Netherlands', 'Sweden', 'Poland', 'Mexico', 'South Korea',
        'Singapore', 'Turkey', 'Indonesia', 'Thailand'
    ]
    
    # CPU models for servers
    CPU_MODELS = [
        'Intel Xeon E5-2680 v4', 'Intel Xeon Gold 6248', 'AMD EPYC 7542',
        'Intel Xeon Platinum 8275CL', 'AMD EPYC 7763'
    ]
    
    # VPN protocols
    PROTOCOLS = ['WireGuard', 'OpenVPN', 'IKEv2', 'NordLynx']
    
    def __init__(self, num_servers=150, num_days=365, sessions_per_day=50000):
        self.num_servers = num_servers
        self.num_days = num_days
        self.sessions_per_day = sessions_per_day
        self.start_date = datetime.now() - timedelta(days=num_days)
    
    def generate_providers(self):
        """Generate provider records"""
        return self.PROVIDERS.copy()
    
    def generate_platforms(self):
        """Generate platform records"""
        return [{'name': p['name'], 'display_name': p['display_name'], 'is_mobile': p['is_mobile']} 
                for p in self.PLATFORMS]
    
    def generate_servers(self, providers):
        """Generate VPN server infrastructure"""
        servers = []
        provider_ids = list(range(1, len(providers) + 1))
        
        for i in range(self.num_servers):
            city, country = random.choice(self.LOCATIONS)
            provider_id = random.choice(provider_ids)
            
            # Generate hostname like: us-nyc-001.prod.surfshark.com
            country_code = country[:2].lower()
            city_code = city[:3].lower()
            server_num = str(i).zfill(3)  # Use actual index to avoid duplicates
            hostname = f"{country_code}-{city_code}-{server_num}.prod.surfshark.com"
            
            server = {
                'hostname': hostname,
                'ip_address': fake.ipv4(),
                'provider_id': provider_id,
                'location_country': country,
                'location_city': city,
                'cpu_model': random.choice(self.CPU_MODELS),
                'cpu_cores': random.choice([8, 16, 32, 64]),
                'ram_gb': random.choice([32, 64, 128, 256]),
                'is_active': True,
                'created_at': self.start_date - timedelta(days=random.randint(30, 365))
            }
            servers.append(server)
        
        return servers
    
    def generate_sessions_for_day(self, current_date, servers):
        """Generate VPN sessions for a single day with realistic trends"""
        sessions = []
        
        # Calculate days since start for growth calculation
        days_elapsed = (current_date - self.start_date).days
        
        # Add organic growth trend (2% monthly growth = ~0.066% daily)
        growth_factor = 1 + (days_elapsed * 0.0007)  # 0.07% daily growth
        
        # Add seasonal variation (sine wave with 90-day period)
        seasonal_factor = 1 + 0.15 * np.sin(2 * np.pi * days_elapsed / 90)
        
        # Add random daily variation (-10% to +10%)
        random_factor = 1 + random.uniform(-0.1, 0.1)
        
        # Vary sessions by day of week (weekends have fewer sessions)
        day_of_week = current_date.weekday()
        if day_of_week >= 5:  # Weekend
            weekday_factor = 0.7
        else:
            weekday_factor = 1.0
        
        # Calculate final session count
        base_sessions = self.sessions_per_day
        num_sessions = int(base_sessions * growth_factor * seasonal_factor * weekday_factor * random_factor)
        
        for _ in range(num_sessions):
            # Random time during the day with peak hours
            hour_probs = [0.02, 0.01, 0.01, 0.01, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06,
                          0.07, 0.06, 0.05, 0.05, 0.05, 0.06, 0.07, 0.08, 0.08, 0.07,
                          0.06, 0.05, 0.04, 0.03]
            # Normalize to ensure sum is exactly 1.0
            hour_probs = np.array(hour_probs)
            hour_probs = hour_probs / hour_probs.sum()
            
            hour = int(np.random.choice(range(24), p=hour_probs))
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            
            created_at = current_date.replace(hour=hour, minute=minute, second=second)
            
            # Select platform
            platform_weights = [p['weight'] for p in self.PLATFORMS]
            platform = np.random.choice(self.PLATFORMS, p=platform_weights)
            
            # Generate session
            session = self._generate_single_session(created_at, servers, platform)
            sessions.append(session)
        
        return sessions
    
    def _generate_single_session(self, created_at, servers, platform):
        """Generate a single VPN session with realistic metrics"""
        server = random.choice(servers)
        
        # Session ID
        session_id = str(uuid.uuid4())
        
        # App version
        major = random.randint(3, 5)
        minor = random.randint(0, 9)
        patch = random.randint(0, 20)
        app_version = f"{platform['name']} {major}.{minor}.{patch}"
        
        # Device model (for mobile)
        device_model = None
        if platform['is_mobile']:
            if platform['name'] == 'ios':
                device_model = random.choice(['iPhone 13', 'iPhone 14', 'iPhone 15', 'iPad Pro'])
            else:
                device_model = random.choice(['SM-G998B', 'Pixel 7', 'OnePlus 11', 'Xiaomi 13'])
        
        # User country
        user_country = random.choice(self.USER_COUNTRIES)
        
        # Connection flow
        has_connect_intent = random.random() < 0.98  # 98% have intent
        is_connected = False
        is_canceled = False
        connect_intent_at = None
        connected_at = None
        disconnected_at = None
        canceled_at = None
        connection_duration_seconds = 0
        connected_protocol = None
        
        # Performance tracking
        connect_intent_trigger = None
        connecting_time_ms = None
        disconnect_intent_at = None
        disconnect_intent_trigger = None
        
        if has_connect_intent:
            connect_intent_at = created_at + timedelta(seconds=random.randint(1, 5))
            
            # Intent trigger types (weighted by frequency)
            connect_intent_trigger = random.choices(
                ['user_action', 'auto_connect', 'quick_connect', 'reconnect'],
                weights=[0.6, 0.2, 0.15, 0.05]
            )[0]
            
            # 95% connectivity rate
            if random.random() < 0.95:
                is_connected = True
                # Connection time (latency: 500ms - 10 seconds, weighted toward faster)
                connecting_time_ms = int(np.random.gamma(2, 1000))  # Gamma distribution for realistic latency
                connecting_time_ms = min(connecting_time_ms, 10000)  # Cap at 10 seconds
                
                connected_at = connect_intent_at + timedelta(milliseconds=connecting_time_ms)
                connected_protocol = random.choice(self.PROTOCOLS)
                
                # Session duration (5 minutes to 4 hours)
                duration_minutes = int(np.random.exponential(scale=45)) + 5
                duration_minutes = min(duration_minutes, 240)  # Cap at 4 hours
                connection_duration_seconds = duration_minutes * 60
                
                # Disconnect tracking
                disconnect_intent_at = connected_at + timedelta(seconds=connection_duration_seconds - random.randint(1, 5))
                disconnect_intent_trigger = random.choices(
                    ['user_action', 'app_close', 'switch_server', 'network_change', 'timeout'],
                    weights=[0.5, 0.2, 0.15, 0.1, 0.05]
                )[0]
                
                disconnected_at = disconnect_intent_at + timedelta(seconds=random.randint(1, 3))
            else:
                # Canceled connection
                is_canceled = True
                canceled_at = connect_intent_at + timedelta(seconds=random.randint(10, 30))
                connecting_time_ms = None  # No connection established
        
        # Quality metrics
        nonet_event_count = 0
        nonet_total_duration_ms = 0
        reconnect_event_count = 0
        unexpected_disconnect = False
        
        if is_connected:
            # 10% chance of network issues
            if random.random() < 0.10:
                nonet_event_count = random.randint(1, 5)
                nonet_total_duration_ms = nonet_event_count * random.randint(500, 5000)
            
            # 5% chance of reconnection events
            if random.random() < 0.05:
                reconnect_event_count = random.randint(1, 3)
            
            # 2% chance of unexpected disconnect
            if random.random() < 0.02:
                unexpected_disconnect = True
        
        # User ratings (5% of sessions get rated)
        has_user_rating = random.random() < 0.05
        is_negative_rating = False
        if has_user_rating:
            # 20% of ratings are negative
            is_negative_rating = random.random() < 0.20
        
        return {
            'session_id': session_id,
            'server_id': server['id'],
            'app_name': platform['name'],
            'app_version': app_version,
            'device_model': device_model,
            'user_country': user_country,
            'created_at': created_at,
            'connect_intent_at': connect_intent_at,
            'connected_at': connected_at,
            'disconnected_at': disconnected_at,
            'canceled_at': canceled_at,
            'connected_protocol': connected_protocol,
            'connection_duration_seconds': connection_duration_seconds,
            # Performance tracking fields
            'connect_intent_trigger': connect_intent_trigger,
            'connecting_time_ms': connecting_time_ms,
            'disconnect_intent_at': disconnect_intent_at,
            'disconnect_intent_trigger': disconnect_intent_trigger,
            # Quality metrics
            'has_connect_intent': has_connect_intent,
            'is_connected': is_connected,
            'is_canceled': is_canceled,
            'nonet_event_count': nonet_event_count,
            'nonet_total_duration_ms': nonet_total_duration_ms,
            'reconnect_event_count': reconnect_event_count,
            'unexpected_disconnect': unexpected_disconnect,
            'has_user_rating': has_user_rating,
            'is_negative_rating': is_negative_rating
        }
    
    def generate_server_costs_for_day(self, current_date, servers, sessions_by_server, providers):
        """Generate daily cost records for each server"""
        cost_records = []
        
        for server in servers:
            server_id = server['id']
            provider = providers[server['provider_id'] - 1]
            
            # Daily base cost (monthly cost / 30)
            base_cost = provider['cost_per_server_monthly'] / 30.0
            
            # Get sessions for this server on this day
            server_sessions = sessions_by_server.get(server_id, [])
            total_sessions = len(server_sessions)
            
            # Calculate connection hours
            total_seconds = sum(s.get('connection_duration_seconds', 0) for s in server_sessions)
            total_connection_hours = total_seconds / 3600.0
            
            # Estimate data transfer (assume 50MB per hour of connection)
            total_gb_transferred = (total_connection_hours * 50) / 1024.0
            
            # Transfer cost
            transfer_cost = total_gb_transferred * provider['cost_per_gb_transfer']
            
            # Total cost
            total_cost = base_cost + transfer_cost
            
            cost_record = {
                'server_id': server_id,
                'date': current_date.date(),
                'base_cost': base_cost,
                'transfer_cost': transfer_cost,
                'total_cost': total_cost,
                'total_sessions': total_sessions,
                'total_connection_hours': total_connection_hours,
                'total_gb_transferred': total_gb_transferred
            }
            cost_records.append(cost_record)
        
        return cost_records