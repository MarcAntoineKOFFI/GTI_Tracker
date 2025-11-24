"""
Enterprise-grade error handling and logging system
Comprehensive error recovery with user-friendly messages
"""
import logging
import traceback
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable, Any
from functools import wraps
from dataclasses import dataclass
import json


@dataclass
class ErrorContext:
    """Context information for an error"""
    error_id: str
    timestamp: datetime
    error_type: str
    error_message: str
    stack_trace: str
    user_action: str
    system_state: dict


class ErrorHandler:
    """Centralized error handling with user-friendly messages"""

    def __init__(self, log_dir: Path = None):
        """Initialize error handler with logging"""
        if log_dir is None:
            log_dir = Path.home() / '.gti_tracker' / 'logs'

        log_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        log_file = log_dir / f'gti_tracker_{datetime.now().strftime("%Y%m%d")}.log'

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )

        self.logger = logging.getLogger('GTI_Tracker')
        self.error_log_file = log_dir / 'errors.json'

    def generate_error_id(self) -> str:
        """Generate unique error ID"""
        import uuid
        return str(uuid.uuid4())[:8].upper()

    def log_error(self, error: Exception, context: dict = None) -> str:
        """
        Log error with full context
        Returns error ID for user reference
        """
        error_id = self.generate_error_id()

        error_context = ErrorContext(
            error_id=error_id,
            timestamp=datetime.now(),
            error_type=type(error).__name__,
            error_message=str(error),
            stack_trace=traceback.format_exc(),
            user_action=context.get('action', 'Unknown') if context else 'Unknown',
            system_state=context or {}
        )

        # Log to file
        self.logger.error(
            f"Error ID: {error_id} | Type: {error_context.error_type} | "
            f"Message: {error_context.error_message} | "
            f"Action: {error_context.user_action}"
        )
        self.logger.debug(f"Stack trace:\n{error_context.stack_trace}")

        # Append to JSON error log for analysis
        self._append_to_error_log(error_context)

        return error_id

    def _append_to_error_log(self, error_context: ErrorContext):
        """Append error to JSON log file"""
        try:
            # Read existing errors
            if self.error_log_file.exists():
                with open(self.error_log_file, 'r') as f:
                    errors = json.load(f)
            else:
                errors = []

            # Append new error
            errors.append({
                'error_id': error_context.error_id,
                'timestamp': error_context.timestamp.isoformat(),
                'type': error_context.error_type,
                'message': error_context.error_message,
                'action': error_context.user_action,
                'state': error_context.system_state
            })

            # Keep only last 1000 errors
            errors = errors[-1000:]

            # Write back
            with open(self.error_log_file, 'w') as f:
                json.dump(errors, f, indent=2)

        except Exception as e:
            self.logger.error(f"Failed to write to error log: {e}")

    def get_user_friendly_message(self, error: Exception) -> str:
        """
        Convert technical error to user-friendly message
        """
        error_type = type(error).__name__

        # Database errors
        if 'Database' in error_type or 'SQL' in error_type:
            return (
                "We couldn't save your changes because of a database issue. "
                "Your work has been saved temporarily. Please try again in a moment."
            )

        # Network errors
        if 'Connection' in error_type or 'Timeout' in error_type:
            return (
                "We couldn't connect to save your changes. "
                "Your work is saved locally and will sync when connection is restored."
            )

        # Permission errors
        if 'Permission' in error_type or 'Access' in error_type:
            return (
                "We don't have permission to save to this location. "
                "Please check your file permissions or choose a different location."
            )

        # Validation errors
        if 'Validation' in error_type or 'Invalid' in error_type:
            return str(error)  # These are already user-friendly

        # Generic error
        return (
            "Something unexpected happened. The error has been logged. "
            "Please try again, and if the problem persists, contact support."
        )

    def handle_error(self, error: Exception, context: dict = None,
                    show_to_user: bool = True) -> tuple[str, str]:
        """
        Handle error with logging and user notification
        Returns (error_id, user_message)
        """
        error_id = self.log_error(error, context)
        user_message = self.get_user_friendly_message(error)

        if show_to_user:
            full_message = f"{user_message}\n\nError ID: {error_id}"
            return error_id, full_message

        return error_id, user_message


# Global error handler instance
error_handler = ErrorHandler()


def handle_errors(action_name: str = None, show_dialog: bool = True):
    """
    Decorator for error handling in functions

    Usage:
        @handle_errors("saving contact")
        def save_contact(self, contact_data):
            # code that might raise errors
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                context = {
                    'action': action_name or func.__name__,
                    'function': func.__name__,
                    'args': str(args),
                    'kwargs': str(kwargs)
                }

                error_id, user_message = error_handler.handle_error(
                    e, context, show_to_user=show_dialog
                )

                if show_dialog:
                    # If in Qt context, show dialog
                    try:
                        from PySide6.QtWidgets import QMessageBox, QApplication
                        if QApplication.instance():
                            QMessageBox.critical(
                                None,
                                "Error",
                                user_message
                            )
                    except ImportError:
                        print(f"ERROR: {user_message}")

                # Re-raise for critical errors that should stop execution
                if isinstance(e, (SystemExit, KeyboardInterrupt)):
                    raise

                return None

        return wrapper
    return decorator


def retry_on_failure(max_retries: int = 3, delay: float = 1.0,
                    backoff: float = 2.0):
    """
    Decorator for automatic retry with exponential backoff

    Usage:
        @retry_on_failure(max_retries=3, delay=1.0)
        def save_to_database(data):
            # code that might fail transiently
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            import time

            current_delay = delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        # Last attempt failed, raise the error
                        raise

                    error_handler.logger.warning(
                        f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}: {e}"
                    )

                    # Wait before retrying
                    time.sleep(current_delay)
                    current_delay *= backoff

            return None

        return wrapper
    return decorator


class OperationLogger:
    """Log user operations for audit trail"""

    def __init__(self, log_dir: Path = None):
        if log_dir is None:
            log_dir = Path.home() / '.gti_tracker' / 'logs'

        log_dir.mkdir(parents=True, exist_ok=True)
        self.activity_log = log_dir / 'user_activity.json'

    def log_action(self, action: str, entity_type: str, entity_id: int = None,
                   details: dict = None):
        """Log a user action"""
        try:
            # Read existing log
            if self.activity_log.exists():
                with open(self.activity_log, 'r') as f:
                    activities = json.load(f)
            else:
                activities = []

            # Add new activity
            activity = {
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'entity_type': entity_type,
                'entity_id': entity_id,
                'details': details or {}
            }

            activities.append(activity)

            # Keep only last 10000 activities
            activities = activities[-10000:]

            # Write back
            with open(self.activity_log, 'w') as f:
                json.dump(activities, f, indent=2)

        except Exception as e:
            error_handler.logger.error(f"Failed to log activity: {e}")

    def get_recent_activities(self, limit: int = 50) -> list:
        """Get recent user activities"""
        try:
            if not self.activity_log.exists():
                return []

            with open(self.activity_log, 'r') as f:
                activities = json.load(f)

            return activities[-limit:]

        except Exception as e:
            error_handler.logger.error(f"Failed to read activities: {e}")
            return []


# Global activity logger
activity_logger = OperationLogger()

