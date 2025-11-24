"""
Validation utilities
"""
import re
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """
    Validate if a string is a valid URL

    Args:
        url: URL string to validate

    Returns:
        True if valid URL
    """
    if not url:
        return True  # Empty URL is considered valid (optional field)

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def is_valid_email(email: str) -> bool:
    """
    Validate if a string is a valid email

    Args:
        email: Email string to validate

    Returns:
        True if valid email
    """
    if not email:
        return True  # Empty email is valid (optional)

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_required_field(value: str, field_name: str) -> tuple[bool, str]:
    """
    Validate that a required field is not empty

    Args:
        value: Field value
        field_name: Name of the field for error message

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value or not value.strip():
        return False, f"{field_name} is required"
    return True, ""


def validate_text_length(
    value: str,
    max_length: int,
    field_name: str
) -> tuple[bool, str]:
    """
    Validate text length

    Args:
        value: Text value
        max_length: Maximum allowed length
        field_name: Name of the field for error message

    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(value) > max_length:
        return False, f"{field_name} must be {max_length} characters or less"
    return True, ""

