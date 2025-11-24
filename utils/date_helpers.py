"""
Date helper utilities
"""
from datetime import date, datetime, timedelta
from typing import Optional


def days_since(target_date: date) -> int:
    """
    Calculate days between target date and today

    Args:
        target_date: The date to compare against

    Returns:
        Number of days since target_date
    """
    return (date.today() - target_date).days


def format_date(dt: date, format_str: str = "%b %d, %Y") -> str:
    """
    Format a date nicely

    Args:
        dt: Date to format
        format_str: strftime format string

    Returns:
        Formatted date string
    """
    return dt.strftime(format_str)


def get_week_bucket(dt: date) -> tuple[date, date]:
    """
    Get the Monday-Sunday week bucket for a given date

    Args:
        dt: Date to bucket

    Returns:
        Tuple of (week_start, week_end) dates
    """
    # Get Monday of the week
    days_since_monday = dt.weekday()
    week_start = dt - timedelta(days=days_since_monday)
    week_end = week_start + timedelta(days=6)
    return week_start, week_end


def get_last_n_days(n: int, end_date: Optional[date] = None) -> list[date]:
    """
    Get list of the last N days

    Args:
        n: Number of days
        end_date: End date (default: today)

    Returns:
        List of dates in chronological order
    """
    if end_date is None:
        end_date = date.today()

    return [end_date - timedelta(days=i) for i in range(n-1, -1, -1)]


def get_last_n_weeks(n: int) -> list[tuple[date, date]]:
    """
    Get list of the last N weeks (Monday-Sunday)

    Args:
        n: Number of weeks

    Returns:
        List of (week_start, week_end) tuples
    """
    weeks = []
    today = date.today()

    for i in range(n-1, -1, -1):
        week_end = today - timedelta(days=i*7)
        week_start, week_end = get_week_bucket(week_end)
        weeks.append((week_start, week_end))

    return weeks


def format_date_short(dt: date) -> str:
    """
    Format date in short format (e.g., "Mon 18")

    Args:
        dt: Date to format

    Returns:
        Formatted date string
    """
    return dt.strftime("%a %d")


def is_future_date(dt: date) -> bool:
    """
    Check if a date is in the future

    Args:
        dt: Date to check

    Returns:
        True if date is in the future
    """
    return dt > date.today()

