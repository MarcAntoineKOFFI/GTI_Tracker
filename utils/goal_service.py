"""
Goal Tracking Service for daily contact goals
"""
from datetime import date
from db.session import get_session
from db.models import NetworkingContact, Settings
from sqlalchemy import func


class GoalTrackingService:
    
    @staticmethod
    def get_daily_goal() -> int:
        session = get_session()
        try:
            settings = session.query(Settings).filter_by(id=1).first()
            return settings.daily_goal if (settings and hasattr(settings, 'daily_goal')) else 3
        finally:
            session.close()
    
    @staticmethod
    def get_today_count() -> int:
        session = get_session()
        try:
            today = date.today()
            count = session.query(NetworkingContact).filter(
                func.date(NetworkingContact.contact_date) == today
            ).count()
            return count
        finally:
            session.close()
    
    @staticmethod
    def get_remaining_today() -> int:
        goal = GoalTrackingService.get_daily_goal()
        today_count = GoalTrackingService.get_today_count()
        remaining = goal - today_count
        return max(0, remaining)
    
    @staticmethod
    def get_progress_percentage() -> float:
        goal = GoalTrackingService.get_daily_goal()
        if goal == 0:
            return 100.0
        today_count = GoalTrackingService.get_today_count()
        return min(100.0, (today_count / goal) * 100)
