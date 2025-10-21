#!/usr/bin/env python3
"""Generate VPN session and cost data for Surfshark Analytics"""
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.data_layer.config import AppConfig
from shared.data_layer.models import db, Provider, VPNServer, VPNSession, ServerCost, Platform
from shared.data_generators.vpn_data_generator import VPNDataGenerator
from flask import Flask

def create_app():
    """Create Flask app for database operations"""
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    db.init_app(app)
    return app

def generate_data(num_servers=150, num_days=365, sessions_per_day=50000):
    """Generate all VPN data"""
    print("\n🚀 Starting Surfshark VPN Data Generation...")
    print(f"   Servers: {num_servers}")
    print(f"   Days: {num_days}")
    print(f"   Sessions/day: {sessions_per_day:,}")
    print(f"   Total sessions: {num_days * sessions_per_day:,}\n")
    
    app = create_app()
    
    with app.app_context():
        # Create tables
        print("📊 Creating database tables...")
        db.create_all()
        print("   ✅ Tables created\n")
        
        # Initialize generator
        generator = VPNDataGenerator(
            num_servers=num_servers,
            num_days=num_days,
            sessions_per_day=sessions_per_day
        )
        
        # Generate providers
        print("🏢 Generating providers...")
        provider_data = generator.generate_providers()
        for p_data in provider_data:
            provider = Provider(**p_data)
            db.session.add(provider)
        db.session.commit()
        providers = Provider.query.all()
        print(f"   ✅ Created {len(providers)} providers\n")
        
        # Generate platforms
        print("📱 Generating platforms...")
        platform_data = generator.generate_platforms()
        for p_data in platform_data:
            platform = Platform(**p_data)
            db.session.add(platform)
        db.session.commit()
        platforms = Platform.query.all()
        print(f"   ✅ Created {len(platforms)} platforms\n")
        
        # Generate servers
        print("🖥️  Generating VPN servers...")
        server_data = generator.generate_servers(provider_data)
        for s_data in server_data:
            server = VPNServer(**s_data)
            db.session.add(server)
        db.session.commit()
        servers = VPNServer.query.all()
        print(f"   ✅ Created {len(servers)} servers\n")
        
        # Convert servers to dict format for generator
        servers_dict = [{
            'id': s.id,
            'hostname': s.hostname,
            'provider_id': s.provider_id,
            'location_country': s.location_country,
            'location_city': s.location_city
        } for s in servers]
        
        # Generate sessions and costs day by day
        print("🔄 Generating VPN sessions and costs...")
        print("   This may take a few minutes...\n")
        
        start_date = generator.start_date
        total_sessions_created = 0
        total_costs_created = 0
        
        for day_num in range(num_days):
            current_date = start_date + timedelta(days=day_num)
            
            # Generate sessions for this day
            sessions = generator.generate_sessions_for_day(current_date, servers_dict)
            
            # Group sessions by server for cost calculation
            sessions_by_server = defaultdict(list)
            for session_data in sessions:
                server_id = session_data['server_id']
                sessions_by_server[server_id].append(session_data)
                
                # Add session to database
                session = VPNSession(**session_data)
                db.session.add(session)
            
            # Generate costs for this day
            cost_records = generator.generate_server_costs_for_day(
                current_date, servers_dict, sessions_by_server, provider_data
            )
            
            for cost_data in cost_records:
                cost = ServerCost(**cost_data)
                db.session.add(cost)
            
            # Commit every day
            db.session.commit()
            
            total_sessions_created += len(sessions)
            total_costs_created += len(cost_records)
            
            # Progress update every 30 days
            if (day_num + 1) % 30 == 0 or day_num == num_days - 1:
                progress = ((day_num + 1) / num_days) * 100
                print(f"   Progress: {progress:.1f}% - Day {day_num + 1}/{num_days} - "
                      f"Sessions: {total_sessions_created:,} - Costs: {total_costs_created:,}")
        
        print("\n✅ Data generation complete!\n")
        print("📈 Summary:")
        print(f"   Providers: {len(providers)}")
        print(f"   Platforms: {len(platforms)}")
        print(f"   Servers: {len(servers)}")
        print(f"   Sessions: {total_sessions_created:,}")
        print(f"   Cost Records: {total_costs_created:,}")
        
        # Calculate some stats
        total_cost = db.session.query(db.func.sum(ServerCost.total_cost)).scalar() or 0
        avg_daily_cost = total_cost / num_days if num_days > 0 else 0
        
        print(f"\n💰 Cost Summary:")
        print(f"   Total Infrastructure Cost: ${total_cost:,.2f}")
        print(f"   Average Daily Cost: ${avg_daily_cost:,.2f}")
        print(f"   Average Cost per Session: ${total_cost / total_sessions_created:.4f}")
        
        print("\n🎉 Ready to start the Cost Analytics app!")
        print("\nNext steps:")
        print("   1. cd cost-app/backend")
        print("   2. python app.py")
        print("   3. In new terminal: cd cost-app/frontend && npm start\n")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate VPN session and cost data')
    parser.add_argument('--servers', type=int, default=150, help='Number of servers (default: 150)')
    parser.add_argument('--days', type=int, default=365, help='Number of days (default: 365)')
    parser.add_argument('--sessions-per-day', type=int, default=50000, 
                       help='Sessions per day (default: 50000)')
    
    args = parser.parse_args()
    
    try:
        generate_data(
            num_servers=args.servers,
            num_days=args.days,
            sessions_per_day=args.sessions_per_day
        )
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)