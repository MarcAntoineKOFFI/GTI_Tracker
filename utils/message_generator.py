"""
Message generation utilities
"""
from typing import Optional
from db.models import NetworkingContact, Settings
from db.session import get_session


def generate_networking_message(
    contact: NetworkingContact,
    settings: Optional[Settings] = None
) -> str:
    """
    Generate a networking message from template and contact/user data

    Args:
        contact: NetworkingContact object
        settings: Settings object (if None, will fetch from DB)

    Returns:
        Generated message string
    """
    if settings is None:
        session = get_session()
        try:
            settings = session.query(Settings).filter_by(id=1).first()
        finally:
            session.close()

    if not settings:
        return "Error: Settings not found"

    template = settings.message_template

    # Prepare replacement values
    replacements = {
        'name': contact.name or '',
        'job_title': contact.job_title or '',
        'company': contact.company or '',
        'user_name': settings.user_name or 'Your Name',
        'user_school': settings.user_school or 'Your University',
        'user_ambitions': settings.user_ambitions or '',
        'relevant_info': contact.relevant_info or ''
    }

    # Replace placeholders
    message = template
    for key, value in replacements.items():
        placeholder = '{' + key + '}'
        message = message.replace(placeholder, value)

    return message


def get_template_placeholders() -> list[str]:
    """
    Get list of available template placeholders

    Returns:
        List of placeholder strings
    """
    return [
        '{name}',
        '{job_title}',
        '{company}',
        '{user_name}',
        '{user_school}',
        '{user_ambitions}',
        '{relevant_info}'
    ]

