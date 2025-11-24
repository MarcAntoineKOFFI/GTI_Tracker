"""
Performance optimization utilities
Lazy loading, caching, and query optimization
"""
from typing import Any, Callable, Dict, Optional
from datetime import datetime, timedelta
from functools import wraps
import time
import logging

logger = logging.getLogger('GTI_Tracker.Performance')


class Cache:
    """Simple in-memory cache with TTL"""

    def __init__(self, default_ttl: int = 30):
        """
        Initialize cache

        Args:
            default_ttl: Default time-to-live in seconds
        """
        self._cache: Dict[str, tuple[Any, datetime]] = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key not in self._cache:
            self.misses += 1
            return None

        value, expiry = self._cache[key]

        if datetime.now() > expiry:
            # Expired, remove and return None
            del self._cache[key]
            self.misses += 1
            return None

        self.hits += 1
        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache"""
        if ttl is None:
            ttl = self.default_ttl

        expiry = datetime.now() + timedelta(seconds=ttl)
        self._cache[key] = (value, expiry)

    def invalidate(self, key: str):
        """Remove key from cache"""
        if key in self._cache:
            del self._cache[key]

    def clear(self):
        """Clear entire cache"""
        self._cache.clear()
        self.hits = 0
        self.misses = 0

    def get_stats(self) -> dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0

        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'size': len(self._cache)
        }


# Global cache instance
global_cache = Cache(default_ttl=30)


def cached(ttl: int = 30, key_func: Optional[Callable] = None):
    """
    Decorator for caching function results

    Args:
        ttl: Time-to-live in seconds
        key_func: Optional function to generate cache key from args

    Usage:
        @cached(ttl=60)
        def expensive_query():
            return session.query(...).all()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # Check cache
            cached_value = global_cache.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_value

            # Execute function
            logger.debug(f"Cache miss for {func.__name__}, executing...")
            result = func(*args, **kwargs)

            # Store in cache
            global_cache.set(cache_key, result, ttl)

            return result

        return wrapper
    return decorator


def measure_time(func: Callable) -> Callable:
    """
    Decorator to measure function execution time

    Usage:
        @measure_time
        def slow_operation():
            # code
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start

        if elapsed > 0.1:  # Log if > 100ms
            logger.warning(f"{func.__name__} took {elapsed*1000:.2f}ms")
        else:
            logger.debug(f"{func.__name__} took {elapsed*1000:.2f}ms")

        return result

    return wrapper


class LazyLoader:
    """Lazy loading for large datasets"""

    def __init__(self, page_size: int = 50):
        """
        Initialize lazy loader

        Args:
            page_size: Number of items per page
        """
        self.page_size = page_size
        self.current_page = 0
        self.total_items = 0
        self.loaded_items = []

    def load_page(self, data_source: Callable, page: int = 0) -> list:
        """
        Load a specific page of data

        Args:
            data_source: Function that returns full dataset
            page: Page number to load

        Returns:
            List of items for the page
        """
        all_data = data_source()
        self.total_items = len(all_data)

        start_idx = page * self.page_size
        end_idx = start_idx + self.page_size

        return all_data[start_idx:end_idx]

    def has_next_page(self) -> bool:
        """Check if there are more pages"""
        return (self.current_page + 1) * self.page_size < self.total_items

    def has_previous_page(self) -> bool:
        """Check if there are previous pages"""
        return self.current_page > 0


class QueryOptimizer:
    """Query optimization utilities"""

    @staticmethod
    def add_indexes(engine):
        """
        Add database indexes for frequently queried columns

        Args:
            engine: SQLAlchemy engine
        """
        from sqlalchemy import Index, text

        indexes = [
            # Networking contacts
            "CREATE INDEX IF NOT EXISTS idx_networking_status ON networking_contacts(status)",
            "CREATE INDEX IF NOT EXISTS idx_networking_date ON networking_contacts(contact_date)",
            "CREATE INDEX IF NOT EXISTS idx_networking_company ON networking_contacts(company)",

            # Internship applications
            "CREATE INDEX IF NOT EXISTS idx_internship_status ON internship_applications(status)",
            "CREATE INDEX IF NOT EXISTS idx_internship_date ON internship_applications(application_date)",
            "CREATE INDEX IF NOT EXISTS idx_internship_company ON internship_applications(company)",
            "CREATE INDEX IF NOT EXISTS idx_internship_contact ON internship_applications(contact_id)",
        ]

        with engine.connect() as conn:
            for idx_sql in indexes:
                try:
                    conn.execute(text(idx_sql))
                    conn.commit()
                except Exception as e:
                    logger.error(f"Failed to create index: {e}")

        logger.info("Database indexes created/verified")

    @staticmethod
    def analyze_query_plan(session, query):
        """
        Analyze query execution plan

        Args:
            session: SQLAlchemy session
            query: Query object to analyze
        """
        from sqlalchemy import text

        # Get query SQL
        sql = str(query.statement.compile(
            compile_kwargs={"literal_binds": True}
        ))

        # Explain query
        explain_sql = f"EXPLAIN QUERY PLAN {sql}"
        result = session.execute(text(explain_sql))

        logger.info("Query execution plan:")
        for row in result:
            logger.info(str(row))


class PerformanceMonitor:
    """Monitor application performance metrics"""

    def __init__(self):
        self.metrics = {
            'db_queries': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'slow_operations': []
        }

    def record_query(self, duration: float):
        """Record database query"""
        self.metrics['db_queries'] += 1

        if duration > 0.1:  # Slow query threshold
            self.metrics['slow_operations'].append({
                'type': 'query',
                'duration': duration,
                'timestamp': datetime.now()
            })

    def get_stats(self) -> dict:
        """Get performance statistics"""
        stats = self.metrics.copy()
        stats['cache_stats'] = global_cache.get_stats()
        return stats

    def reset(self):
        """Reset metrics"""
        self.metrics = {
            'db_queries': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'slow_operations': []
        }


# Global performance monitor
perf_monitor = PerformanceMonitor()


def debounce(wait_ms: int = 300):
    """
    Debounce decorator for functions
    Delays execution until after wait_ms milliseconds have elapsed since last call

    Args:
        wait_ms: Milliseconds to wait

    Usage:
        @debounce(300)
        def on_text_changed(text):
            # expensive operation
    """
    def decorator(func: Callable) -> Callable:
        timer = None

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal timer

            from PySide6.QtCore import QTimer

            if timer is not None:
                timer.stop()

            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(lambda: func(*args, **kwargs))
            timer.start(wait_ms)

        return wrapper
    return decorator


def throttle(interval_ms: int = 1000):
    """
    Throttle decorator for functions
    Ensures function is called at most once per interval

    Args:
        interval_ms: Minimum milliseconds between calls

    Usage:
        @throttle(1000)
        def on_scroll(position):
            # load more data
    """
    def decorator(func: Callable) -> Callable:
        last_called = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_called
            now = time.time() * 1000

            if now - last_called >= interval_ms:
                last_called = now
                return func(*args, **kwargs)

        return wrapper
    return decorator

