from datetime import date, timedelta
from typing import Tuple

def get_last_7_days() -> Tuple[date, date]:
    end = date.today()
    start = end - timedelta(days=7)
    return start, end

def get_last_30_days() -> Tuple[date, date]:
    end = date.today()
    start = end - timedelta(days=30)
    return start, end

def get_last_90_days() -> Tuple[date, date]:
    end = date.today()
    start = end - timedelta(days=90)
    return start, end
