"""Executive dashboard API endpoints and logic"""
from datetime import timedelta
from shared.data_layer.repositories import ServerCostRepository, VPNSessionRepository
from shared.utils.helpers import get_date_range_from_params, safe_divide

def get_executive_summary(days=30):
    """Get executive summary with cost KPIs and comparisons
    
    Args:
        days: Number of days to analyze
        
    Returns:
        Dictionary with executive metrics
    """
    start_date, end_date = get_date_range_from_params(days=days)
    
    # Current period data
    cost_data = ServerCostRepository.get_total_cost(start_date, end_date)
    
    # Previous period for comparison
    prev_start = start_date - timedelta(days=days)
    prev_end = start_date
    prev_cost_data = ServerCostRepository.get_total_cost(prev_start, prev_end)
    
    # Calculate period-over-period changes
    total_cost_change = safe_divide(
        (cost_data['total_cost'] - prev_cost_data['total_cost']),
        prev_cost_data['total_cost'],
        0.0
    ) * 100
    
    cost_per_session_change = safe_divide(
        (cost_data['cost_per_session'] - prev_cost_data['cost_per_session']),
        prev_cost_data['cost_per_session'],
        0.0
    ) * 100
    
    cost_per_hour_change = safe_divide(
        (cost_data['cost_per_hour'] - prev_cost_data['cost_per_hour']),
        prev_cost_data['cost_per_hour'],
        0.0
    ) * 100
    
    # Calculate efficiency metrics
    avg_daily_cost = cost_data['total_cost'] / days if days > 0 else 0
    base_cost_percentage = safe_divide(cost_data['base_cost'], cost_data['total_cost'], 0) * 100
    transfer_cost_percentage = safe_divide(cost_data['transfer_cost'], cost_data['total_cost'], 0) * 100
    
    return {
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'days': days
        },
        'kpis': {
            'total_cost': {
                'current': round(cost_data['total_cost'], 2),
                'previous': round(prev_cost_data['total_cost'], 2),
                'change_percent': round(total_cost_change, 2),
                'trend': 'up' if total_cost_change > 0 else 'down' if total_cost_change < 0 else 'flat'
            },
            'cost_per_session': {
                'current': round(cost_data['cost_per_session'], 4),
                'previous': round(prev_cost_data['cost_per_session'], 4),
                'change_percent': round(cost_per_session_change, 2),
                'trend': 'up' if cost_per_session_change > 0 else 'down' if cost_per_session_change < 0 else 'flat'
            },
            'cost_per_hour': {
                'current': round(cost_data['cost_per_hour'], 4),
                'previous': round(prev_cost_data['cost_per_hour'], 4),
                'change_percent': round(cost_per_hour_change, 2),
                'trend': 'up' if cost_per_hour_change > 0 else 'down' if cost_per_hour_change < 0 else 'flat'
            },
            'avg_daily_cost': {
                'current': round(avg_daily_cost, 2)
            }
        },
        'breakdown': {
            'base_cost': {
                'value': round(cost_data['base_cost'], 2),
                'percentage': round(base_cost_percentage, 1)
            },
            'transfer_cost': {
                'value': round(cost_data['transfer_cost'], 2),
                'percentage': round(transfer_cost_percentage, 1)
            }
        },
        'usage': {
            'total_sessions': cost_data['total_sessions'],
            'total_hours': round(cost_data['total_hours'], 2),
            'avg_session_duration_minutes': round(
                safe_divide(cost_data['total_hours'] * 60, cost_data['total_sessions'], 0),
                1
            )
        }
    }

def get_cost_efficiency_metrics(days=30):
    """Get cost efficiency and optimization metrics
    
    Args:
        days: Number of days to analyze
        
    Returns:
        Dictionary with efficiency metrics
    """
    start_date, end_date = get_date_range_from_params(days=days)
    
    # Get provider costs
    provider_costs = ServerCostRepository.get_cost_by_provider(start_date, end_date)
    
    # Find most and least efficient providers
    if provider_costs:
        sorted_by_efficiency = sorted(provider_costs, key=lambda x: x['cost_per_session'])
        most_efficient = sorted_by_efficiency[0] if sorted_by_efficiency else None
        least_efficient = sorted_by_efficiency[-1] if sorted_by_efficiency else None
    else:
        most_efficient = None
        least_efficient = None
    
    # Get top cost servers
    top_servers = ServerCostRepository.get_top_cost_servers(start_date, end_date, limit=5)
    
    return {
        'most_efficient_provider': most_efficient,
        'least_efficient_provider': least_efficient,
        'top_cost_servers': top_servers,
        'total_providers': len(provider_costs)
    }