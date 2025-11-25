"""
Smart Follow-Up Service with status-based thresholds
"""
from datetime import date, timedelta
from typing import Tuple, List
from db.session import get_session
from db.models import NetworkingContact, NetworkingStatus


class SmartFollowUpService:
    """Intelligent follow-up logic based on status and time"""
    
    # Follow-up thresholds by status (in days)
    THRESHOLDS = {
        NetworkingStatus.COLD_MESSAGE: 3,      # 3 days
        NetworkingStatus.HAS_RESPONDED: 21,   # 3 weeks
        NetworkingStatus.CALL: 21,             # 3 weeks
        NetworkingStatus.INTERVIEW: 7          # 1 week
    }
    
    @staticmethod
    def needs_followup(contact: NetworkingContact) -> bool:
        """Check if contact needs follow-up based on status and time"""
        threshold = SmartFollowUpService.THRESHOLDS.get(contact.status)
        if not threshold:
            return False
        
        days_since = (date.today() - contact.contact_date).days
        return days_since >= threshold
    
    @staticmethod
    def get_followup_contacts() -> List[NetworkingContact]:
        """Get all contacts needing follow-up"""
        session = get_session()
        try:
            all_contacts = session.query(NetworkingContact).all()
            return [c for c in all_contacts if SmartFollowUpService.needs_followup(c)]
        finally:
            session.close()
    
    @staticmethod
    def get_followup_count() -> int:
        """Get count of contacts needing follow-up"""
        return len(SmartFollowUpService.get_followup_contacts())
    
    @staticmethod
    def get_suggested_message(contact: NetworkingContact) -> Tuple[str, str]:
        """Get adaptive message suggestion based on status and timing"""
        days_since = (date.today() - contact.contact_date).days
        
        templates = {
            NetworkingStatus.COLD_MESSAGE: (
                "Initial Follow-Up",
                f"Hi {{name}},\\n\\nI wanted to follow up on my message from {days_since} days ago. "
                f"I'd still love to connect and learn about your experience at {{company}}.\\n\\nBest regards"
            ),
            NetworkingStatus.HAS_RESPONDED: (
                "Continue Conversation",
                f"Hi {{name}},\\n\\nThank you for your previous response! "
                f"I wanted to continue our conversation about {{job_title}} at {{company}}.\\n\\nBest regards"
            ),
            NetworkingStatus.CALL: (
                "Post-Call Follow-Up",
                f"Hi {{name}},\\n\\nThank you so much for taking the time to speak with me! "
                f"I really appreciated your insights about {{company}}. "
                f"As discussed, I'd love to stay in touch.\\n\\nBest regards"
            ),
            NetworkingStatus.INTERVIEW: (
                "Interview Follow-Up",
                f"Hi {{name}},\\n\\nI wanted to thank you again for the interview opportunity. "
                f"I'm very excited about the possibility of joining {{company}}. "
                f"Please let me know if there's any additional information I can provide.\\n\\nBest regards"
            )
        }
        
        return templates.get(contact.status, ("Follow-Up", "Hi {name},\\n\\nJust wanted to follow up.\\n\\nBest regards"))
