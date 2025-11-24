"""
SQLAlchemy ORM models for GTI Tracker
"""
from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime,
    ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()


class NetworkingStatus(enum.Enum):
    """Networking contact status enum"""
    COLD_MESSAGE = "Cold message"
    HAS_RESPONDED = "Has responded"
    CALL = "Call"
    INTERVIEW = "Interview"


class InternshipStatus(enum.Enum):
    """Internship application status enum"""
    APPLIED = "Applied"
    SCREENING = "Screening"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"


class NetworkingContact(Base):
    """Model for networking contacts"""
    __tablename__ = 'networking_contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    contact_date = Column(Date, nullable=False, default=date.today)
    relevant_info = Column(Text, nullable=True)
    status = Column(SQLEnum(NetworkingStatus), nullable=False, default=NetworkingStatus.COLD_MESSAGE)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    last_updated = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationship
    internship_applications = relationship(
        "InternshipApplication",
        back_populates="contact",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<NetworkingContact(id={self.id}, name='{self.name}', company='{self.company}')>"


class InternshipApplication(Base):
    """Model for internship applications"""
    __tablename__ = 'internship_applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    job_link = Column(Text, nullable=True)
    contact_id = Column(Integer, ForeignKey('networking_contacts.id'), nullable=True)
    application_date = Column(Date, nullable=False, default=date.today)
    status = Column(SQLEnum(InternshipStatus), nullable=False, default=InternshipStatus.APPLIED)
    notes = Column(Text, nullable=True)
    last_updated = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationship
    contact = relationship("NetworkingContact", back_populates="internship_applications")

    def __repr__(self):
        return f"<InternshipApplication(id={self.id}, role='{self.role_name}', company='{self.company}')>"


class Settings(Base):
    """Settings table (singleton - only one row should exist)"""
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, default=1)
    message_template = Column(Text, nullable=False)
    follow_up_days = Column(Integer, nullable=False, default=3)
    user_name = Column(String(255), nullable=True)
    user_school = Column(String(255), nullable=True)
    user_ambitions = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Settings(id={self.id}, follow_up_days={self.follow_up_days})>"

