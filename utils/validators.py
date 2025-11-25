"""
Enhanced validators with format checking and error messages
"""
import re
from urllib.parse import urlparse


# Regex patterns
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
LINKEDIN_REGEX = re.compile(r'^(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?$')
PHONE_REGEX = re.compile(r'^\+?[1-9]\d{1,14}$|^\(\d{3}\)\s?\d{3}-?\d{4}$|^\d{3}[-.]?\d{3}[-.]?\d{4}$')


def validate_email(email: str) -> tuple[bool, str]:
    if not email or not email.strip():
        return True, ""
    email = email.strip()
    if EMAIL_REGEX.match(email):
        return True, ""
    return False, "Invalid email format"


def validate_linkedin_url(url: str) -> tuple[bool, str]:
    if not url or not url.strip():
        return True, ""
    url = url.strip()
    if '/' not in url and ' ' not in url:
        return True, ""
    if LINKEDIN_REGEX.match(url):
        return True, ""
    return False, "Invalid LinkedIn URL"


def validate_phone(phone: str) -> tuple[bool, str]:
    if not phone or not phone.strip():
        return True, ""
    phone = phone.strip()
    clean = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('.', '')
    if PHONE_REGEX.match(phone) or (clean.isdigit() and len(clean) >= 10):
        return True, ""
    return False, "Invalid phone format"


def validate_job_url(url: str) -> tuple[bool, str]:
    if not url or not url.strip():
        return True, ""
    url = url.strip()
    try:
        result = urlparse(url)
        if result.scheme and result.netloc:
            return True, ""
        return False, "Must start with http:// or https://"
    except:
        return False, "Invalid URL"


def is_valid_url(url: str) -> bool:
    valid, _ = validate_job_url(url)
    return valid


def is_valid_email(email: str) -> bool:
    valid, _ = validate_email(email)
    return valid


def validate_required_field(value: str, field_name: str) -> tuple[bool, str]:
    if not value or not value.strip():
        return False, f"{field_name} is required"
    return True, ""


def validate_text_length(value: str, max_length: int, field_name: str) -> tuple[bool, str]:
    if len(value) > max_length:
        return False, f"{field_name} must be {max_length} characters or less"
    return True, ""
