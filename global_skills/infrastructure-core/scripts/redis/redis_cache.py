"""
Redis Cache Operations - The Dude S.A.S.
Provides caching functionality with JSON serialization and TTL support.
"""
import json
import logging
from typing import Any, Optional
import redis.asyncio as redis

logger = logging.getLogger(__name__)


async def cache_set(key: str, value: Any, ttl: int = 3600) -> bool:
    """
    Set a cached value with TTL.

    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        ttl: Time to live in seconds (default: 1 hour)

    Returns:
        True if set successfully
    """
    from .redis_client import get_client
    
    try:
        client: redis.Redis = await get_client()
        serialized = json.dumps(value)
        await client.setex(key, ttl, serialized)
        logger.info(f"Cached {key} with TTL {ttl}s")
        return True
    except Exception as e:
        logger.error(f"Failed to cache {key}: {str(e)}")
        raise


async def cache_get(key: str) -> Optional[Any]:
    """
    Get a cached value.

    Args:
        key: Cache key

    Returns:
        Cached value or None if not found/expired
    """
    from .redis_client import get_client
    
    try:
        client: redis.Redis = await get_client()
        value = await client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        logger.error(f"Failed to get cache {key}: {str(e)}")
        raise


async def cache_invalidate(pattern: str) -> int:
    """
    Invalidate all keys matching a pattern.

    Args:
        pattern: Key pattern (e.g., 'user:*')

    Returns:
        Number of keys deleted
    """
    from .redis_client import get_client
    
    try:
        client: redis.Redis = await get_client()
        keys = await client.keys(pattern)
        if keys:
            count = await client.delete(*keys)
            logger.info(f"Invalidated {count} keys matching {pattern}")
            return count
        return 0
    except Exception as e:
        logger.error(f"Failed to invalidate {pattern}: {str(e)}")
        raise


async def cache_exists(key: str) -> bool:
    """
    Check if a key exists in cache.

    Args:
        key: Cache key

    Returns:
        True if key exists
    """
    from .redis_client import get_client
    
    try:
        client: redis.Redis = await get_client()
        return await client.exists(key) > 0
    except Exception as e:
        logger.error(f"Failed to check existence of {key}: {str(e)}")
        raise
