from db.session import get_session
from db.models import NetworkingContact

class MilestoneService:
    
    MILESTONES = [
        (10, "🎯 10 Contacts!", "Great start on your networking journey!"),
        (25, "🌟 25 Contacts!", "You're building momentum!"),
        (50, "🚀 50 Contacts!", "Halfway to your first hundred!"),
        (100, "💯 100 Contacts!", "You're a networking champion!"),
    ]
    
    @staticmethod
    def check_milestone(contact_count: int) -> tuple:
        for threshold, title, message in MilestoneService.MILESTONES:
            if contact_count == threshold:
                return (True, title, message)
        return (False, "", "")
    
    @staticmethod
    def get_total_contacts() -> int:
        session = get_session()
        try:
            return session.query(NetworkingContact).count()
        finally:
            session.close()
