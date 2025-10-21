"""Cost calculation service with business logic"""
from datetime import timedelta
from shared.data_layer.repositories import ServerCostRepository, VPNSessionRepository
from shared.utils.helpers import safe_divide

class CostService:
    """Service for cost calculations and business logic"""
    
    @staticmethod
    def calculate_cost_efficiency(total_cost, total_sessions, total_hours):
        """Calculate cost efficiency metrics
        
        Args:
            total_cost: Total infrastructure cost
            total_sessions: Total number of sessions
            total_hours: Total connection hours
            
        Returns:
            Dictionary with efficiency metrics
        """
        return {
            'cost_per_session': safe_divide(total_cost, total_sessions, 0),
            'cost_per_hour': safe_divide(total_cost, total_hours, 0),
            'cost_per_1000_sessions': safe_divide(total_cost * 1000, total_sessions, 0),
            'sessions_per_dollar': safe_divide(total_sessions, total_cost, 0)
        }
    
    @staticmethod
    def calculate_cost_breakdown_percentages(base_cost, transfer_cost):
        """Calculate cost breakdown as percentages
        
        Args:
            base_cost: Base infrastructure cost
            transfer_cost: Data transfer cost
            
        Returns:
            Dictionary with percentage breakdown
        """
        total_cost = base_cost + transfer_cost
        
        return {
            'base_cost_percentage': safe_divide(base_cost, total_cost, 0) * 100,
            'transfer_cost_percentage': safe_divide(transfer_cost, total_cost, 0) * 100,
            'total_cost': total_cost
        }
    
    @staticmethod
    def calculate_period_comparison(current_cost, previous_cost):
        """Calculate period-over-period comparison
        
        Args:
            current_cost: Current period cost data
            previous_cost: Previous period cost data
            
        Returns:
            Dictionary with comparison metrics
        """
        total_cost_change = safe_divide(
            (current_cost['total_cost'] - previous_cost['total_cost']),
            previous_cost['total_cost'],
            0
        ) * 100
        
        cost_per_session_change = safe_divide(
            (current_cost['cost_per_session'] - previous_cost['cost_per_session']),
            previous_cost['cost_per_session'],
            0
        ) * 100
        
        sessions_change = safe_divide(
            (current_cost['total_sessions'] - previous_cost['total_sessions']),
            previous_cost['total_sessions'],
            0
        ) * 100
        
        return {
            'total_cost_change_percent': round(total_cost_change, 2),
            'cost_per_session_change_percent': round(cost_per_session_change, 2),
            'sessions_change_percent': round(sessions_change, 2),
            'trend': 'increasing' if total_cost_change > 5 else 'decreasing' if total_cost_change < -5 else 'stable'
        }
    
    @staticmethod
    def calculate_projected_monthly_cost(daily_avg_cost):
        """Project monthly cost from daily average
        
        Args:
            daily_avg_cost: Average daily cost
            
        Returns:
            Projected monthly cost
        """
        return daily_avg_cost * 30
    
    @staticmethod
    def calculate_cost_per_user_estimate(total_cost, total_sessions, avg_sessions_per_user=10):
        """Estimate cost per user (rough approximation)
        
        Args:
            total_cost: Total infrastructure cost
            total_sessions: Total sessions
            avg_sessions_per_user: Estimated sessions per user
            
        Returns:
            Estimated cost per user
        """
        estimated_users = total_sessions / avg_sessions_per_user
        return safe_divide(total_cost, estimated_users, 0)
    
    @staticmethod
    def identify_cost_anomalies(cost_trend_data, threshold_percentage=20):
        """Identify days with anomalous costs
        
        Args:
            cost_trend_data: List of daily cost records
            threshold_percentage: Percentage deviation to flag as anomaly
            
        Returns:
            List of anomalous days
        """
        if not cost_trend_data or len(cost_trend_data) < 3:
            return []
        
        costs = [d['cost'] for d in cost_trend_data]
        avg_cost = sum(costs) / len(costs)
        
        anomalies = []
        for day in cost_trend_data:
            deviation = abs((day['cost'] - avg_cost) / avg_cost * 100) if avg_cost > 0 else 0
            if deviation > threshold_percentage:
                anomalies.append({
                    'date': day['date'],
                    'cost': day['cost'],
                    'deviation_percent': round(deviation, 2),
                    'type': 'high' if day['cost'] > avg_cost else 'low'
                })
        
        return anomalies
    
    @staticmethod
    def calculate_roi_metrics(total_cost, total_sessions, revenue_per_session=0):
        """Calculate ROI metrics if revenue data is available
        
        Args:
            total_cost: Total infrastructure cost
            total_sessions: Total sessions
            revenue_per_session: Revenue generated per session
            
        Returns:
            Dictionary with ROI metrics
        """
        if revenue_per_session <= 0:
            return {
                'roi_available': False,
                'message': 'Revenue data not available'
            }
        
        total_revenue = total_sessions * revenue_per_session
        profit = total_revenue - total_cost
        roi_percentage = safe_divide(profit, total_cost, 0) * 100
        
        return {
            'roi_available': True,
            'total_revenue': round(total_revenue, 2),
            'total_cost': round(total_cost, 2),
            'profit': round(profit, 2),
            'roi_percentage': round(roi_percentage, 2),
            'profit_margin': round(safe_divide(profit, total_revenue, 0) * 100, 2)
        }