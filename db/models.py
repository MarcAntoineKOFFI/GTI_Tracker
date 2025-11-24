"""
SQLAlchemy ORM models for GTI Tracker
Enterprise-grade data models with ACID compliance, audit trails, and soft deletion
"""
from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime,
    ForeignKey, Enum as SQLEnum, Boolean, event
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declared_attr
import enum

Base = declarative_base()


class AuditMixin:
    """Mixin for audit trail metadata on all entities"""

    @declared_attr
    def created_at(cls):
        return Column(DateTime, nullable=False, default=datetime.now)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    @declared_attr
    def is_deleted(cls):
        return Column(Boolean, nullable=False, default=False)

    @declared_attr
    def deleted_at(cls):
        return Column(DateTime, nullable=True)


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


class NetworkingContact(Base, AuditMixin):
    """Model for networking contacts with full audit trail"""
    __tablename__ = 'networking_contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)  # Length constraint
    job_title = Column(String(150), nullable=False)  # Length constraint
    company = Column(String(150), nullable=False)  # Length constraint
    contact_date = Column(Date, nullable=False, default=date.today)
    relevant_info = Column(Text(1000), nullable=True)  # Max 1000 chars
    status = Column(SQLEnum(NetworkingStatus), nullable=False, default=NetworkingStatus.COLD_MESSAGE)

    # Email and LinkedIn for contact management
    email = Column(String(255), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)

    # Audit trail (from AuditMixin)
    # created_at, updated_at, is_deleted, deleted_at

    # Relationship
    internship_applications = relationship(
        "InternshipApplication",
        back_populates="contact",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<NetworkingContact(id={self.id}, name='{self.name}', company='{self.company}')>"

    def soft_delete(self):
        """Soft delete this contact"""
        self.is_deleted = True
        self.deleted_at = datetime.now()


class InternshipApplication(Base, AuditMixin):
    """Model for internship applications with full audit trail"""
    __tablename__ = 'internship_applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(200), nullable=False)  # Length constraint
    company = Column(String(150), nullable=False)  # Length constraint
    job_link = Column(Text(500), nullable=True)  # URL length constraint
    contact_id = Column(Integer, ForeignKey('networking_contacts.id'), nullable=True)
    application_date = Column(Date, nullable=False, default=date.today)
    status = Column(SQLEnum(InternshipStatus), nullable=False, default=InternshipStatus.APPLIED)
    notes = Column(Text(2000), nullable=True)  # Max 2000 chars

    # Additional tracking fields
    deadline = Column(Date, nullable=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    location = Column(String(200), nullable=True)
    is_remote = Column(Boolean, default=False)

    # Audit trail (from AuditMixin)
    # created_at, updated_at, is_deleted, deleted_at

    # Relationship
    contact = relationship("NetworkingContact", back_populates="internship_applications")

    def __repr__(self):
        return f"<InternshipApplication(id={self.id}, role='{self.role_name}', company='{self.company}')>"

    def soft_delete(self):
        """Soft delete this application"""
        self.is_deleted = True
        self.deleted_at = datetime.now()


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

