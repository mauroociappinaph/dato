"""
Redis Counter Operations - The Dude S.A.S.
Atomic counter management for rate limiting and analytics.
"""
import logging
from typing import Optional
import redis.asyncio as redis


logger = logging.getLogger(__name__)


async def increment_counter(key: str, amount: int = 1) -> int:
    """
    Increment a counter.

    Args:
        key: Counter key
        amount: Amount to increment by

    Returns:
        New counter value
    """
    from .redis_client import get_client
    
    try:
        client: redis.Redis = await get_client()
        value = await client.incrby(key, amount)
        logger.debug(f"Incremented {key} by {amount} to {value}")
        return value
    except Exception as e:
        logger.error(f"Failed to increment {key}: {str(e)}")
        raise


async def get_counter(key: str) -> int:
    """
    Get current counter value.

    Args:
        key: Counter key

    Returns:
        Counter value (0 if not exists)
    """
    from .redis_client import get_client
    
    try:
        client: redis.Redis = await get_client()
        value = await client.get(key)
        return int(value) if value else 0
    except Exception as e:
        logger.error(f"Failed to get counter {key}: {str(e)}")
        raise


async def reset_counter(key: str) -> bool:
    """
    Reset a counter to 0.

    Args:
        key: Counter key

    Returns:
        True if reset
    """
    from .redis_client import get_client
    
    try:
        client: redis.Redis = await get_client()
        await client.set(key, 0)
        logger.info(f"Reset counter {key}")
        return True
    except Exception as e:
        logger.error(f"Failed to reset counter {key}: {str(e)}")
        raise


async def decrement_counter(key: str, amount: int = 1) -> int:
    """
    Decrement a counter.

    Args:
        key: Counter key
        amount: Amount to decrement by

    Returns:
        New counter value
    """
    from .redis_client import get_client
    
    try:
        client: redis.Redis = await get_client()
        value = await client.incrby(key, -amount)
        logger.debug(f"Decremented {key} by {amount} to {value}")
        return value
    except Exception as e:
        logger.error(f"Failed to decrement {key}: {str(e)}")
        raise
