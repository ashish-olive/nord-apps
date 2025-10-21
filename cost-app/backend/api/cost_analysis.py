"""Cost analysis API endpoints and logic"""
from shared.data_layer.repositories import ServerCostRepository, VPNServerRepository
from shared.utils.helpers import get_date_range_from_params, safe_divide

def get_cost_by_provider_analysis(days=30):
    """Get detailed cost analysis by provider
    
    Args:
        days: Number of days to analyze
        
    Returns:
        Dictionary with provider cost analysis
    """
    start_date, end_date = get_date_range_from_params(days=days)
    provider_costs = ServerCostRepository.get_cost_by_provider(start_date, end_date)
    
    # Calculate totals
    total_cost = sum(p['total_cost'] for p in provider_costs)
    total_sessions = sum(p['total_sessions'] for p in provider_costs)
    
    # Enrich with percentages and rankings
    for i, provider in enumerate(provider_costs, 1):
        provider['cost_percentage'] = round(safe_divide(provider['total_cost'], total_cost, 0) * 100, 2)
        provider['session_percentage'] = round(safe_divide(provider['total_sessions'], total_sessions, 0) * 100, 2)
        provider['rank'] = i
        provider['efficiency_score'] = round(
            safe_divide(provider['session_percentage'], provider['cost_percentage'], 0) * 100,
            1
        )
    
    return {
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'days': days
        },
        'summary': {
            'total_cost': round(total_cost, 2),
            'total_sessions': total_sessions,
            'provider_count': len(provider_costs)
        },
        'providers': provider_costs
    }

def get_cost_by_location_analysis(days=30, limit=20):
    """Get detailed cost analysis by geographic location
    
    Args:
        days: Number of days to analyze
        limit: Maximum number of locations to return
        
    Returns:
        Dictionary with location cost analysis
    """
    start_date, end_date = get_date_range_from_params(days=days)
    location_costs = ServerCostRepository.get_cost_by_location(start_date, end_date)
    
    # Sort by total cost descending
    location_costs.sort(key=lambda x: x['total_cost'], reverse=True)
    
    # Limit results
    location_costs = location_costs[:limit]
    
    # Calculate totals
    total_cost = sum(l['total_cost'] for l in location_costs)
    total_sessions = sum(l['total_sessions'] for l in location_costs)
    
    # Enrich with percentages
    for location in location_costs:
        location['cost_percentage'] = round(safe_divide(location['total_cost'], total_cost, 0) * 100, 2)
        location['session_percentage'] = round(safe_divide(location['total_sessions'], total_sessions, 0) * 100, 2)
    
    return {
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'days': days
        },
        'summary': {
            'total_cost': round(total_cost, 2),
            'total_sessions': total_sessions,
            'location_count': len(location_costs)
        },
        'locations': location_costs
    }

def get_server_cost_analysis(days=30, limit=20):
    """Get detailed cost analysis by individual servers
    
    Args:
        days: Number of days to analyze
        limit: Maximum number of servers to return
        
    Returns:
        Dictionary with server cost analysis
    """
    start_date, end_date = get_date_range_from_params(days=days)
    
    # Get top cost servers
    top_servers = ServerCostRepository.get_top_cost_servers(start_date, end_date, limit=limit)
    
    # Calculate totals
    total_cost = sum(s['total_cost'] for s in top_servers)
    total_sessions = sum(s['total_sessions'] for s in top_servers)
    
    # Enrich with additional metrics
    for i, server in enumerate(top_servers, 1):
        server['rank'] = i
        server['cost_percentage'] = round(safe_divide(server['total_cost'], total_cost, 0) * 100, 2)
        server['session_percentage'] = round(safe_divide(server['total_sessions'], total_sessions, 0) * 100, 2)
        server['daily_avg_cost'] = round(server['total_cost'] / days, 2)
        server['daily_avg_sessions'] = round(server['total_sessions'] / days, 1)
    
    return {
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'days': days
        },
        'summary': {
            'total_cost': round(total_cost, 2),
            'total_sessions': total_sessions,
            'avg_cost_per_server': round(safe_divide(total_cost, len(top_servers), 0), 2)
        },
        'servers': top_servers
    }

def get_cost_trends_analysis(days=30):
    """Get cost trends with statistical analysis
    
    Args:
        days: Number of days to analyze
        
    Returns:
        Dictionary with trend analysis
    """
    start_date, end_date = get_date_range_from_params(days=days)
    trends = ServerCostRepository.get_cost_trend(start_date, end_date)
    
    if not trends:
        return {
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            },
            'trends': [],
            'statistics': {}
        }
    
    # Calculate statistics
    costs = [t['cost'] for t in trends]
    sessions = [t['sessions'] for t in trends]
    
    avg_daily_cost = sum(costs) / len(costs) if costs else 0
    max_daily_cost = max(costs) if costs else 0
    min_daily_cost = min(costs) if costs else 0
    
    avg_daily_sessions = sum(sessions) / len(sessions) if sessions else 0
    max_daily_sessions = max(sessions) if sessions else 0
    min_daily_sessions = min(sessions) if sessions else 0
    
    # Calculate trend direction (simple linear)
    if len(costs) >= 2:
        first_half_avg = sum(costs[:len(costs)//2]) / (len(costs)//2)
        second_half_avg = sum(costs[len(costs)//2:]) / (len(costs) - len(costs)//2)
        trend_direction = 'increasing' if second_half_avg > first_half_avg else 'decreasing' if second_half_avg < first_half_avg else 'stable'
        trend_change = round(((second_half_avg - first_half_avg) / first_half_avg * 100) if first_half_avg > 0 else 0, 2)
    else:
        trend_direction = 'stable'
        trend_change = 0
    
    return {
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'days': days
        },
        'trends': trends,
        'statistics': {
            'cost': {
                'average': round(avg_daily_cost, 2),
                'maximum': round(max_daily_cost, 2),
                'minimum': round(min_daily_cost, 2),
                'trend_direction': trend_direction,
                'trend_change_percent': trend_change
            },
            'sessions': {
                'average': round(avg_daily_sessions, 1),
                'maximum': max_daily_sessions,
                'minimum': min_daily_sessions
            }
        }
    }