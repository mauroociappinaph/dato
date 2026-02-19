"""
Redis Session Management - The Dude S.A.S.
Session storage with TTL and automatic cleanup.
"""
import logging
from typing import Optional
from .redis_cache import cache_set, cache_get, cache_exists


logger = logging.getLogger(__name__)


async def store_session(session_id: str, data: dict, ttl: int = 86400) -> bool:
    """
    Store session data.

    Args:
        session_id: Session identifier
        data: Session data dictionary
        ttl: Time to live in seconds (default: 24 hours)

    Returns:
        True if stored successfully
    """
    try:
        key = f"session:{session_id}"
        result = await cache_set(key, data, ttl)
        logger.info(f"Stored session {session_id}")
        return result
    except Exception as e:
        logger.error(f"Failed to store session {session_id}: {str(e)}")
        raise


async def load_session(session_id: str) -> Optional[dict]:
    """
    Load session data.

    Args:
        session_id: Session identifier

    Returns:
        Session data or None if not found/expired
    """
    try:
        key = f"session:{session_id}"
        return await cache_get(key)
    except Exception as e:
        logger.error(f"Failed to load session {session_id}: {str(e)}")
        raise


async def delete_session(session_id: str) -> bool:
    """
    Delete a session.

    Args:
        session_id: Session identifier

    Returns:
        True if deleted
    """
    from .redis_client import get_client
    import redis.asyncio as redis
    
    try:
        client: redis.Redis = await get_client()
        key = f"session:{session_id}"
        await client.delete(key)
        logger.info(f"Deleted session {session_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete session {session_id}: {str(e)}")
        raise


async def session_exists(session_id: str) -> bool:
    """
    Check if a session exists.

    Args:
        session_id: Session identifier

    Returns:
        True if session exists
    """
    key = f"session:{session_id}"
    return await cache_exists(key)
