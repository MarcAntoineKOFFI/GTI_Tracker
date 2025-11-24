"""
Enhanced SQLAlchemy ORM models for GTI Tracker
Includes Task, Interview, Document, CompanyResearch, and ActivityLog models
"""
from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime,
    ForeignKey, Enum as SQLEnum, Float, Boolean, JSON
)
from sqlalchemy.orm import relationship
import enum

# Import base models
from db.models import Base, NetworkingContact, InternshipApplication, Settings

# New Enums

class TaskPriority(enum.Enum):
    """Task priority levels"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class TaskStatus(enum.Enum):
    """Task status"""
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class TaskType(enum.Enum):
    """Task type categories"""
    FOLLOW_UP = "Follow Up"
    APPLY = "Apply"
    RESEARCH = "Research"
    PREPARE_INTERVIEW = "Prepare Interview"
    UPDATE_DOCUMENTS = "Update Documents"
    OTHER = "Other"


class InterviewType(enum.Enum):
    """Interview format types"""
    PHONE = "Phone"
    VIDEO = "Video"
    ON_SITE = "On-Site"
    TECHNICAL = "Technical"
    BEHAVIORAL = "Behavioral"
    CASE = "Case"


class InterviewOutcome(enum.Enum):
    """Interview outcome"""
    PENDING = "Pending"
    PASSED = "Passed"
    REJECTED = "Rejected"
    WAITLISTED = "Waitlisted"


class DocumentType(enum.Enum):
    """Document types"""
    RESUME = "Resume"
    COVER_LETTER = "Cover Letter"
    PORTFOLIO = "Portfolio"
    TRANSCRIPT = "Transcript"
    OTHER = "Other"


class CompanySize(enum.Enum):
    """Company size categories"""
    STARTUP = "Startup (1-50)"
    SMALL = "Small (51-200)"
    MEDIUM = "Medium (201-1000)"
    LARGE = "Large (1001-10000)"
    ENTERPRISE = "Enterprise (10000+)"


class ActivityType(enum.Enum):
    """Activity log types"""
    ADDED_CONTACT = "Added Contact"
    SENT_MESSAGE = "Sent Message"
    UPDATED_STATUS = "Updated Status"
    SUBMITTED_APPLICATION = "Submitted Application"
    HAD_INTERVIEW = "Had Interview"
    RECEIVED_RESPONSE = "Received Response"
    RECEIVED_OFFER = "Received Offer"
    RECEIVED_REJECTION = "Received Rejection"
    CREATED_TASK = "Created Task"
    COMPLETED_TASK = "Completed Task"
    ADDED_NOTE = "Added Note"


class EntityType(enum.Enum):
    """Entity types for activity log"""
    CONTACT = "Contact"
    APPLICATION = "Application"
    INTERVIEW = "Interview"
    TASK = "Task"
    DOCUMENT = "Document"


# New Models

class Task(Base):
    """Model for action items and tasks"""
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=True)
    priority = Column(SQLEnum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    task_type = Column(SQLEnum(TaskType), nullable=False, default=TaskType.OTHER)

    # Optional relationships to contacts/applications
    related_contact_id = Column(Integer, ForeignKey('networking_contacts.id'), nullable=True)
    related_application_id = Column(Integer, ForeignKey('internship_applications.id'), nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)
    reminder_enabled = Column(Boolean, default=True)

    # Relationships
    related_contact = relationship("NetworkingContact", foreign_keys=[related_contact_id])
    related_application = relationship("InternshipApplication", foreign_keys=[related_application_id])

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status.value}')>"


class Interview(Base):
    """Model for tracking interview rounds"""
    __tablename__ = 'interviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey('internship_applications.id'), nullable=False)
    interview_round = Column(Integer, nullable=False, default=1)
    interview_type = Column(SQLEnum(InterviewType), nullable=False)
    scheduled_date = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    interviewer_names = Column(Text, nullable=True)
    preparation_notes = Column(Text, nullable=True)
    questions_asked = Column(Text, nullable=True)
    performance_self_rating = Column(Integer, nullable=True)  # 1-5 scale
    outcome = Column(SQLEnum(InterviewOutcome), nullable=False, default=InterviewOutcome.PENDING)
    follow_up_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    # Relationship
    application = relationship("InternshipApplication", back_populates="interviews")

    def __repr__(self):
        return f"<Interview(id={self.id}, round={self.interview_round}, type='{self.interview_type.value}')>"


class Document(Base):
    """Model for document version control"""
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_type = Column(SQLEnum(DocumentType), nullable=False)
    file_path = Column(Text, nullable=False)
    version_number = Column(Integer, nullable=False, default=1)
    created_date = Column(DateTime, nullable=False, default=datetime.now)
    last_used_date = Column(DateTime, nullable=True)
    tailored_for_company = Column(String(255), nullable=True)
    tailored_for_role = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Document(id={self.id}, type='{self.document_type.value}', v{self.version_number})>"


class CompanyResearch(Base):
    """Model for centralized company intelligence"""
    __tablename__ = 'company_research'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False, unique=True)
    industry = Column(String(255), nullable=True)
    company_size = Column(SQLEnum(CompanySize), nullable=True)
    culture_notes = Column(Text, nullable=True)
    recent_news = Column(Text, nullable=True)
    products_services = Column(Text, nullable=True)
    key_competitors = Column(Text, nullable=True)
    interview_process_notes = Column(Text, nullable=True)
    glassdoor_rating = Column(Float, nullable=True)
    average_salary_range = Column(String(100), nullable=True)
    website_url = Column(String(500), nullable=True)
    careers_page_url = Column(String(500), nullable=True)
    last_updated = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<CompanyResearch(id={self.id}, company='{self.company_name}')>"


class ActivityLog(Base):
    """Model for comprehensive activity tracking"""
    __tablename__ = 'activity_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.now)
    activity_type = Column(SQLEnum(ActivityType), nullable=False)
    entity_type = Column(SQLEnum(EntityType), nullable=False)
    entity_id = Column(Integer, nullable=False)
    details = Column(JSON, nullable=True)  # Flexible JSON field for additional context
    user_note = Column(Text, nullable=True)

    def __repr__(self):
        return f"<ActivityLog(id={self.id}, type='{self.activity_type.value}', entity='{self.entity_type.value}')>"


# Add relationship to InternshipApplication for interviews
InternshipApplication.interviews = relationship(
    "Interview",
    back_populates="application",
    cascade="all, delete-orphan"
)

