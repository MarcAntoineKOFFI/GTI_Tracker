"""
Database session management and initialization
Enterprise-grade with automatic backups
"""
import os
import sys
import logging
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db.models import Base, Settings

logger = logging.getLogger(__name__)

# Global backup manager instance
_backup_manager = None


def get_app_data_dir() -> Path:
    """
    Get OS-appropriate application data directory

    Returns:
        Path to application data directory
    """
    if sys.platform == 'win32':
        # Windows: %APPDATA%\GTI_Tracker
        base_dir = os.getenv('APPDATA')
        if not base_dir:
            base_dir = os.path.expanduser('~\\AppData\\Roaming')
        app_dir = Path(base_dir) / 'GTI_Tracker'
    elif sys.platform == 'darwin':
        # macOS: ~/Library/Application Support/GTI_Tracker
        app_dir = Path.home() / 'Library' / 'Application Support' / 'GTI_Tracker'
    else:
        # Linux: ~/.local/share/GTI_Tracker (XDG base directory)
        xdg_data_home = os.getenv('XDG_DATA_HOME')
        if xdg_data_home:
            app_dir = Path(xdg_data_home) / 'GTI_Tracker'
        else:
            app_dir = Path.home() / '.local' / 'share' / 'GTI_Tracker'

    # Create directory if it doesn't exist
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


def get_database_path() -> Path:
    """Get the full path to the database file"""
    return get_app_data_dir() / 'gti_tracker.db'


# Global engine and session factory
_engine = None
_SessionFactory = None


def init_database() -> None:
    """
    Initialize the database:
    - Create engine
    - Create all tables if they don't exist
    - Insert default settings if needed
    - Initialize backup manager and perform scheduled backups
    """
    global _engine, _SessionFactory, _backup_manager

    db_path = get_database_path()
    db_exists = db_path.exists()

    logger.info(f"Database path: {db_path}")
    logger.info(f"Database exists: {db_exists}")

    # Create engine
    _engine = create_engine(f'sqlite:///{db_path}', echo=False)
    _SessionFactory = sessionmaker(bind=_engine)

    # Create all tables
    Base.metadata.create_all(_engine)
    logger.info("Database tables created/verified")

    # Run migrations if needed
    if db_exists:
        try:
            from db.migrations import run_migrations
            run_migrations()
        except Exception as e:
            logger.warning(f"Migration failed: {e}")

    # Create indexes for performance
    try:
        from utils.performance import QueryOptimizer
        QueryOptimizer.add_indexes(_engine)
    except Exception as e:
        logger.warning(f"Failed to create indexes: {e}")

    # Initialize backup manager
    try:
        from utils.backup_manager import BackupManager
        _backup_manager = BackupManager(db_path)

        # Perform scheduled backups if database exists
        if db_exists:
            _backup_manager.perform_scheduled_backups()
            logger.info("Scheduled backups completed")
    except Exception as e:
        logger.warning(f"Backup manager initialization failed: {e}")

    # If this is a new database, insert default settings
    if not db_exists:
        _insert_default_settings()


def _insert_default_settings() -> None:
    """Insert default settings row into the database"""
    default_template = """Hi {name},

I hope this message finds you well! My name is {user_name}, and I'm currently a student at {user_school}. I came across your profile and was really impressed by your work as a {job_title} at {company}.

{user_ambitions}

{relevant_info}

I would love to learn more about your experience and any advice you might have for someone looking to break into the field. Would you be open to a brief chat sometime?

Thank you for your time and consideration!

Best regards,
{user_name}"""

    session = get_session()
    try:
        settings = Settings(
            id=1,
            message_template=default_template,
            follow_up_days=3,
            user_name="Your Name",
            user_school="Your University",
            user_ambitions="I'm passionate about breaking into the tech industry and gaining hands-on experience through internships."
        )
        session.add(settings)
        session.commit()
        logger.info("Default settings inserted")
    except Exception as e:
        session.rollback()
        logger.error(f"Error inserting default settings: {e}")
        raise
    finally:
        session.close()


def get_session() -> Session:
    """
    Get a new database session

    Returns:
        SQLAlchemy Session object
    """
    if _SessionFactory is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    return _SessionFactory()


def get_engine():
    """Get the database engine"""
    return _engine


def get_backup_manager():
    """Get the backup manager instance"""
    return _backup_manager


def create_manual_backup():
    """Create a manual backup of the database"""
    if _backup_manager:
        return _backup_manager.create_backup('manual', compress=True)
    return None


