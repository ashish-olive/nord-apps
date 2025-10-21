"""Scenario modeling API for cost what-if analysis"""
from shared.data_layer.repositories import ServerCostRepository, ProviderRepository
from shared.utils.helpers import get_date_range_from_params, safe_divide

def calculate_scenario(scenario_params, days=30):
    """Calculate cost impact of a scenario
    
    Args:
        scenario_params: Dictionary with scenario parameters
            - scenario_type: 'server_scaling', 'provider_migration', 'traffic_growth', 'cost_optimization'
            - parameters: Scenario-specific parameters
        days: Number of days for baseline
        
    Returns:
        Dictionary with scenario impact analysis
    """
    scenario_type = scenario_params.get('scenario_type')
    parameters = scenario_params.get('parameters', {})
    
    # Get baseline data
    start_date, end_date = get_date_range_from_params(days=days)
    baseline_cost = ServerCostRepository.get_total_cost(start_date, end_date)
    
    if scenario_type == 'server_scaling':
        return calculate_server_scaling_scenario(baseline_cost, parameters, days)
    elif scenario_type == 'provider_migration':
        return calculate_provider_migration_scenario(baseline_cost, parameters, days)
    elif scenario_type == 'traffic_growth':
        return calculate_traffic_growth_scenario(baseline_cost, parameters, days)
    elif scenario_type == 'cost_optimization':
        return calculate_cost_optimization_scenario(baseline_cost, parameters, days)
    else:
        return {
            'error': 'Invalid scenario type',
            'valid_types': ['server_scaling', 'provider_migration', 'traffic_growth', 'cost_optimization']
        }

def calculate_server_scaling_scenario(baseline_cost, parameters, days):
    """Calculate impact of adding/removing servers
    
    Args:
        baseline_cost: Current cost data
        parameters: {'server_change': int, 'provider': str}
        days: Number of days
        
    Returns:
        Scenario impact
    """
    server_change = parameters.get('server_change', 0)
    provider_name = parameters.get('provider', 'AWS')
    
    # Get provider pricing
    providers = ProviderRepository.get_all_providers()
    provider = next((p for p in providers if p.name == provider_name), None)
    
    if not provider:
        return {'error': f'Provider {provider_name} not found'}
    
    # Calculate additional cost
    daily_cost_per_server = provider.cost_per_server_monthly / 30
    additional_daily_cost = server_change * daily_cost_per_server
    additional_total_cost = additional_daily_cost * days
    
    # Assume proportional session distribution
    current_servers = baseline_cost['total_sessions'] / 100  # Rough estimate
    new_servers = current_servers + server_change
    session_capacity_change = safe_divide(server_change, current_servers, 0) * 100
    
    new_total_cost = baseline_cost['total_cost'] + additional_total_cost
    new_cost_per_session = safe_divide(new_total_cost, baseline_cost['total_sessions'], 0)
    
    cost_change_percent = safe_divide(
        (new_total_cost - baseline_cost['total_cost']),
        baseline_cost['total_cost'],
        0
    ) * 100
    
    return {
        'scenario_type': 'server_scaling',
        'parameters': {
            'server_change': server_change,
            'provider': provider_name,
            'action': 'add' if server_change > 0 else 'remove'
        },
        'baseline': {
            'total_cost': round(baseline_cost['total_cost'], 2),
            'cost_per_session': round(baseline_cost['cost_per_session'], 4),
            'total_sessions': baseline_cost['total_sessions']
        },
        'projected': {
            'total_cost': round(new_total_cost, 2),
            'cost_per_session': round(new_cost_per_session, 4),
            'additional_cost': round(additional_total_cost, 2),
            'cost_change_percent': round(cost_change_percent, 2),
            'capacity_change_percent': round(session_capacity_change, 2)
        },
        'recommendation': 'Proceed' if cost_change_percent < 10 else 'Review' if cost_change_percent < 20 else 'Caution'
    }

def calculate_provider_migration_scenario(baseline_cost, parameters, days):
    """Calculate impact of migrating servers between providers
    
    Args:
        baseline_cost: Current cost data
        parameters: {'from_provider': str, 'to_provider': str, 'server_percentage': float}
        days: Number of days
        
    Returns:
        Scenario impact
    """
    from_provider_name = parameters.get('from_provider')
    to_provider_name = parameters.get('to_provider')
    migration_percentage = parameters.get('server_percentage', 0) / 100
    
    providers = ProviderRepository.get_all_providers()
    from_provider = next((p for p in providers if p.name == from_provider_name), None)
    to_provider = next((p for p in providers if p.name == to_provider_name), None)
    
    if not from_provider or not to_provider:
        return {'error': 'Provider not found'}
    
    # Calculate cost difference
    from_daily_cost = from_provider.cost_per_server_monthly / 30
    to_daily_cost = to_provider.cost_per_server_monthly / 30
    
    cost_diff_per_server = (to_daily_cost - from_daily_cost) * days
    
    # Estimate number of servers to migrate (rough estimate)
    estimated_servers = baseline_cost['total_sessions'] / 1000
    servers_to_migrate = estimated_servers * migration_percentage
    
    total_cost_impact = cost_diff_per_server * servers_to_migrate
    new_total_cost = baseline_cost['total_cost'] + total_cost_impact
    
    cost_change_percent = safe_divide(total_cost_impact, baseline_cost['total_cost'], 0) * 100
    
    return {
        'scenario_type': 'provider_migration',
        'parameters': {
            'from_provider': from_provider_name,
            'to_provider': to_provider_name,
            'migration_percentage': parameters.get('server_percentage', 0)
        },
        'baseline': {
            'total_cost': round(baseline_cost['total_cost'], 2)
        },
        'projected': {
            'total_cost': round(new_total_cost, 2),
            'cost_impact': round(total_cost_impact, 2),
            'cost_change_percent': round(cost_change_percent, 2),
            'monthly_savings': round(-total_cost_impact * 30 / days, 2) if total_cost_impact < 0 else 0
        },
        'recommendation': 'Proceed' if total_cost_impact < 0 else 'Not recommended'
    }

def calculate_traffic_growth_scenario(baseline_cost, parameters, days):
    """Calculate impact of traffic/session growth
    
    Args:
        baseline_cost: Current cost data
        parameters: {'growth_percentage': float}
        days: Number of days
        
    Returns:
        Scenario impact
    """
    growth_percentage = parameters.get('growth_percentage', 0) / 100
    
    # Assume transfer costs grow proportionally with traffic
    new_transfer_cost = baseline_cost['transfer_cost'] * (1 + growth_percentage)
    new_total_cost = baseline_cost['base_cost'] + new_transfer_cost
    
    new_sessions = baseline_cost['total_sessions'] * (1 + growth_percentage)
    new_cost_per_session = safe_divide(new_total_cost, new_sessions, 0)
    
    cost_change_percent = safe_divide(
        (new_total_cost - baseline_cost['total_cost']),
        baseline_cost['total_cost'],
        0
    ) * 100
    
    return {
        'scenario_type': 'traffic_growth',
        'parameters': {
            'growth_percentage': parameters.get('growth_percentage', 0)
        },
        'baseline': {
            'total_cost': round(baseline_cost['total_cost'], 2),
            'total_sessions': baseline_cost['total_sessions'],
            'cost_per_session': round(baseline_cost['cost_per_session'], 4)
        },
        'projected': {
            'total_cost': round(new_total_cost, 2),
            'total_sessions': round(new_sessions),
            'cost_per_session': round(new_cost_per_session, 4),
            'cost_change_percent': round(cost_change_percent, 2),
            'additional_cost': round(new_total_cost - baseline_cost['total_cost'], 2)
        },
        'recommendation': 'Plan capacity' if growth_percentage > 0.2 else 'Monitor'
    }

def calculate_cost_optimization_scenario(baseline_cost, parameters, days):
    """Calculate impact of cost optimization measures
    
    Args:
        baseline_cost: Current cost data
        parameters: {'optimization_percentage': float}
        days: Number of days
        
    Returns:
        Scenario impact
    """
    optimization_percentage = parameters.get('optimization_percentage', 0) / 100
    
    # Apply optimization to both base and transfer costs
    new_base_cost = baseline_cost['base_cost'] * (1 - optimization_percentage)
    new_transfer_cost = baseline_cost['transfer_cost'] * (1 - optimization_percentage)
    new_total_cost = new_base_cost + new_transfer_cost
    
    new_cost_per_session = safe_divide(new_total_cost, baseline_cost['total_sessions'], 0)
    
    savings = baseline_cost['total_cost'] - new_total_cost
    savings_percent = safe_divide(savings, baseline_cost['total_cost'], 0) * 100
    
    return {
        'scenario_type': 'cost_optimization',
        'parameters': {
            'optimization_percentage': parameters.get('optimization_percentage', 0)
        },
        'baseline': {
            'total_cost': round(baseline_cost['total_cost'], 2),
            'cost_per_session': round(baseline_cost['cost_per_session'], 4)
        },
        'projected': {
            'total_cost': round(new_total_cost, 2),
            'cost_per_session': round(new_cost_per_session, 4),
            'savings': round(savings, 2),
            'savings_percent': round(savings_percent, 2),
            'monthly_savings': round(savings * 30 / days, 2)
        },
        'recommendation': 'Implement' if savings > 0 else 'Not applicable'
    }