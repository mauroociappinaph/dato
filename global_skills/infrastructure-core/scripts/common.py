"""
Common utilities for infrastructure operations.
"""

import logging
from typing import Any, Callable, TypeVar, Optional
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)

T = TypeVar('T')


def with_retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator to retry async functions on failure.

    Args:
        max_attempts: Maximum number of attempts
        delay: Delay between attempts in seconds
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {delay}s..."
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}: {str(e)}"
                        )

            raise last_exception

        return wrapper
    return decorator


def validate_required_env(*vars: str) -> None:
    """
    Validate that required environment variables are set.

    Args:
        *vars: Variable names to check

    Raises:
        ValueError: If any variable is missing
    """
    import os
    missing = [var for var in vars if not os.getenv(var)]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


class InfraError(Exception):
    """Base exception for infrastructure errors."""
    pass


class CacheError(InfraError):
    """Exception for cache-related errors."""
    pass


class DatabaseError(InfraError):
    """Exception for database-related errors."""
    pass
