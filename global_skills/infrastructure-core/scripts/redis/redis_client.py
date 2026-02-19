"""
Redis Client Management - The Dude S.A.S.
Singleton pattern for Redis connection with async support.
"""
import os
import logging
from typing import Optional
import redis.asyncio as redis

logger = logging.getLogger(__name__)

# Singleton client
_redis_client: Optional[redis.Redis] = None


async def get_client() -> redis.Redis:
    """Get or create Redis client singleton."""
    global _redis_client
    if _redis_client is None:
        redis_url = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')
        _redis_client = await redis.from_url(redis_url, decode_responses=True)
        logger.info(f"Redis client created: {redis_url}")
    return _redis_client
