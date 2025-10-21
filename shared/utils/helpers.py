"""Utility helper functions for Surfshark VPN Analytics"""
from datetime import datetime, timedelta, date
from typing import Tuple

def get_date_range(days: int) -> Tuple[datetime, datetime]:
    """Get date range for the last N days
    
    Args:
        days: Number of days to look back
        
    Returns:
        Tuple of (start_date, end_date) as datetime objects
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

def get_date_range_from_params(days: int = None, start_date: str = None, end_date: str = None) -> Tuple[date, date]:
    """Get date range from request parameters
    
    Args:
        days: Number of days to look back (if provided)
        start_date: Start date string in YYYY-MM-DD format
        end_date: End date string in YYYY-MM-DD format
        
    Returns:
        Tuple of (start_date, end_date) as date objects
    """
    if start_date and end_date:
        # Use provided date range
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    elif days:
        # Use days parameter
        end = date.today()
        start = end - timedelta(days=days)
    else:
        # Default to last 30 days
        end = date.today()
        start = end - timedelta(days=30)
    
    return start, end

def format_currency(amount: float) -> str:
    """Format amount as currency
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted currency string
    """
    return f"${amount:,.2f}"

def format_percentage(value: float, decimals: int = 2) -> str:
    """Format value as percentage
    
    Args:
        value: Value to format (0-100)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{value:.{decimals}f}%"

def calculate_percentage_change(current: float, previous: float) -> float:
    """Calculate percentage change between two values
    
    Args:
        current: Current value
        previous: Previous value
        
    Returns:
        Percentage change (positive or negative)
    """
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if denominator is zero
        
    Returns:
        Result of division or default value
    """
    if denominator == 0:
        return default
    return numerator / denominator