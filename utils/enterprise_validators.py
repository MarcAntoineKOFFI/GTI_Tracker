"""
Enterprise-grade input validation system
Comprehensive validation with user-friendly error messages
"""
import re
from datetime import date, datetime
from typing import Optional, Tuple, List
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of a validation check"""
    is_valid: bool
    error_message: Optional[str] = None
    suggestions: Optional[List[str]] = None


class InputValidator:
    """Comprehensive input validation with intelligent error messages"""

    # Common email typos
    EMAIL_DOMAIN_CORRECTIONS = {
        'gmial': 'gmail',
        'gmai': 'gmail',
        'gamil': 'gmail',
        'yahooo': 'yahoo',
        'yaho': 'yahoo',
        'outloo': 'outlook',
        'hotmial': 'hotmail',
    }

    @staticmethod
    def validate_name(name: str) -> ValidationResult:
        """
        Validate person or company name
        Must be 2-100 characters, no numbers
        """
        if not name or not name.strip():
            return ValidationResult(False, "Name is required")

        name = name.strip()

        if len(name) < 2:
            return ValidationResult(False, "Name must be at least 2 characters")

        if len(name) > 100:
            return ValidationResult(False, "Name must be 100 characters or less")

        # Check for excessive numbers (names can have "John Smith III")
        if sum(c.isdigit() for c in name) > 3:
            return ValidationResult(False, "Name contains too many numbers")

        return ValidationResult(True)

    @staticmethod
    def validate_job_title(title: str) -> ValidationResult:
        """
        Validate job title
        Must be 2-150 characters
        """
        if not title or not title.strip():
            return ValidationResult(False, "Job title is required")

        title = title.strip()

        if len(title) < 2:
            return ValidationResult(False, "Job title must be at least 2 characters")

        if len(title) > 150:
            return ValidationResult(False, "Job title must be 150 characters or less")

        return ValidationResult(True)

    @staticmethod
    def validate_company_name(company: str) -> ValidationResult:
        """
        Validate company name
        Must be 2-150 characters
        """
        if not company or not company.strip():
            return ValidationResult(False, "Company name is required")

        company = company.strip()

        if len(company) < 2:
            return ValidationResult(False, "Company name must be at least 2 characters")

        if len(company) > 150:
            return ValidationResult(False, "Company name must be 150 characters or less")

        return ValidationResult(True)

    @staticmethod
    def validate_email(email: str) -> ValidationResult:
        """
        Validate email address with typo detection
        """
        if not email:
            return ValidationResult(True)  # Email is optional

        email = email.strip().lower()

        # Basic email regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_pattern, email):
            return ValidationResult(False, "Please enter a valid email address")

        # Check for common domain typos
        domain = email.split('@')[1]
        domain_name = domain.split('.')[0]

        if domain_name in InputValidator.EMAIL_DOMAIN_CORRECTIONS:
            correct_domain = InputValidator.EMAIL_DOMAIN_CORRECTIONS[domain_name]
            suggestion = email.replace(domain_name, correct_domain)
            return ValidationResult(
                True,
                None,
                [f"Did you mean {suggestion}?"]
            )

        return ValidationResult(True)

    @staticmethod
    def validate_url(url: str) -> ValidationResult:
        """
        Validate URL format
        """
        if not url:
            return ValidationResult(True)  # URL is optional

        url = url.strip()

        # Must start with http:// or https://
        if not url.startswith(('http://', 'https://')):
            return ValidationResult(
                False,
                "URL must start with http:// or https://",
                [f"https://{url}"]
            )

        # Basic URL pattern
        url_pattern = r'https?://[^\s]+'
        if not re.match(url_pattern, url):
            return ValidationResult(False, "Please enter a valid URL")

        if len(url) > 500:
            return ValidationResult(False, "URL is too long (max 500 characters)")

        return ValidationResult(True)

    @staticmethod
    def validate_phone(phone: str) -> ValidationResult:
        """
        Validate phone number
        Accepts various formats, normalizes to digits
        """
        if not phone:
            return ValidationResult(True)  # Phone is optional

        # Remove common separators
        digits = re.sub(r'[^\d+]', '', phone)

        if len(digits) < 10:
            return ValidationResult(False, "Phone number must have at least 10 digits")

        if len(digits) > 15:
            return ValidationResult(False, "Phone number is too long")

        return ValidationResult(True)

    @staticmethod
    def validate_date(date_value: date, field_name: str = "Date") -> ValidationResult:
        """
        Validate date is reasonable
        """
        if not date_value:
            return ValidationResult(False, f"{field_name} is required")

        # Check it's not too far in past
        if date_value.year < 2020:
            return ValidationResult(False, f"{field_name} seems too far in the past")

        # Check it's not in future (for contact dates)
        if field_name.lower() in ['contact date', 'application date']:
            if date_value > date.today():
                return ValidationResult(False, f"{field_name} cannot be in the future")

        return ValidationResult(True)

    @staticmethod
    def validate_text_length(text: str, max_length: int, field_name: str = "Text") -> ValidationResult:
        """
        Validate text doesn't exceed maximum length
        """
        if not text:
            return ValidationResult(True)  # Optional field

        if len(text) > max_length:
            return ValidationResult(
                False,
                f"{field_name} must be {max_length} characters or less (currently {len(text)})"
            )

        return ValidationResult(True)

    @staticmethod
    def normalize_company_name(company: str) -> str:
        """
        Normalize company name for consistency
        - Trim whitespace
        - Title case
        - Remove common suffixes for matching
        """
        if not company:
            return ""

        # Trim and title case
        normalized = company.strip().title()

        # Replace common variations
        replacements = {
            ' Inc.': ' Inc',
            ' Inc ': ' Inc',
            ' Incorporated': ' Inc',
            ' Corp.': ' Corp',
            ' Corp ': ' Corp',
            ' Corporation': ' Corp',
            ' LLC': '',
            ' Ltd': '',
            ' Limited': '',
        }

        for old, new in replacements.items():
            normalized = normalized.replace(old, new)

        return normalized.strip()

    @staticmethod
    def calculate_string_similarity(str1: str, str2: str) -> float:
        """
        Calculate similarity between two strings (0.0 to 1.0)
        Using Levenshtein distance ratio
        """
        if not str1 or not str2:
            return 0.0

        str1 = str1.lower()
        str2 = str2.lower()

        if str1 == str2:
            return 1.0

        # Simple implementation of Levenshtein distance
        len1, len2 = len(str1), len(str2)
        if len1 == 0:
            return len2
        if len2 == 0:
            return len1

        matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]

        for i in range(len1 + 1):
            matrix[i][0] = i
        for j in range(len2 + 1):
            matrix[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if str1[i-1] == str2[j-1] else 1
                matrix[i][j] = min(
                    matrix[i-1][j] + 1,      # deletion
                    matrix[i][j-1] + 1,      # insertion
                    matrix[i-1][j-1] + cost  # substitution
                )

        distance = matrix[len1][len2]
        max_len = max(len1, len2)

        return 1.0 - (distance / max_len)

    @staticmethod
    def validate_salary_range(min_salary: Optional[int], max_salary: Optional[int]) -> ValidationResult:
        """
        Validate salary range is reasonable
        """
        if min_salary is not None and max_salary is not None:
            if min_salary > max_salary:
                return ValidationResult(False, "Minimum salary cannot be greater than maximum salary")

            if min_salary < 0:
                return ValidationResult(False, "Salary cannot be negative")

            if max_salary > 500000:  # Reasonable upper bound for internships
                return ValidationResult(False, "Maximum salary seems unreasonably high for an internship")

        return ValidationResult(True)


class FormValidator:
    """High-level form validation orchestrator"""

    @staticmethod
    def validate_contact_form(name: str, job_title: str, company: str,
                             contact_date: date, email: str = None,
                             phone: str = None) -> Tuple[bool, dict]:
        """
        Validate complete contact form
        Returns (is_valid, errors_dict)
        """
        errors = {}

        # Validate each field
        name_result = InputValidator.validate_name(name)
        if not name_result.is_valid:
            errors['name'] = name_result.error_message

        title_result = InputValidator.validate_job_title(job_title)
        if not title_result.is_valid:
            errors['job_title'] = title_result.error_message

        company_result = InputValidator.validate_company_name(company)
        if not company_result.is_valid:
            errors['company'] = company_result.error_message

        date_result = InputValidator.validate_date(contact_date, "Contact date")
        if not date_result.is_valid:
            errors['contact_date'] = date_result.error_message

        if email:
            email_result = InputValidator.validate_email(email)
            if not email_result.is_valid:
                errors['email'] = email_result.error_message

        if phone:
            phone_result = InputValidator.validate_phone(phone)
            if not phone_result.is_valid:
                errors['phone'] = phone_result.error_message

        return (len(errors) == 0, errors)

    @staticmethod
    def validate_application_form(role_name: str, company: str,
                                 application_date: date, job_link: str = None,
                                 deadline: date = None,
                                 salary_min: int = None,
                                 salary_max: int = None) -> Tuple[bool, dict]:
        """
        Validate complete application form
        Returns (is_valid, errors_dict)
        """
        errors = {}

        # Validate required fields
        role_result = InputValidator.validate_name(role_name)
        if not role_result.is_valid:
            errors['role_name'] = role_result.error_message

        company_result = InputValidator.validate_company_name(company)
        if not company_result.is_valid:
            errors['company'] = company_result.error_message

        date_result = InputValidator.validate_date(application_date, "Application date")
        if not date_result.is_valid:
            errors['application_date'] = date_result.error_message

        # Validate optional fields
        if job_link:
            url_result = InputValidator.validate_url(job_link)
            if not url_result.is_valid:
                errors['job_link'] = url_result.error_message

        # Validate deadline is after application date
        if deadline and application_date:
            if deadline < application_date:
                errors['deadline'] = "Deadline cannot be before application date"

        # Validate salary range
        salary_result = InputValidator.validate_salary_range(salary_min, salary_max)
        if not salary_result.is_valid:
            errors['salary'] = salary_result.error_message

        return (len(errors) == 0, errors)

