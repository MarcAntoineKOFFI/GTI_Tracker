"""
Contact History Model for tracking status changes
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from db.models import Base, NetworkingStatus


class ContactHistory(Base):
    """Track history of status changes for contacts"""
    __tablename__ = 'contact_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey('networking_contacts.id'), nullable=False)
    old_status = Column(SQLEnum(NetworkingStatus), nullable=True)
    new_status = Column(SQLEnum(NetworkingStatus), nullable=False)
    changed_at = Column(DateTime, nullable=False, default=datetime.now)
    notes = Column(String(500), nullable=True)
    
    # Relationship
    contact = relationship("NetworkingContact", backref="history")
    
    def __repr__(self):
        return f"<ContactHistory(contact_id={self.contact_id}, status={self.new_status.value}, at={self.changed_at})>"
