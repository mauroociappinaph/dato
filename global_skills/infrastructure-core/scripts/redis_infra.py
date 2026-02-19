"""
Redis Infrastructure Abstractions - DEPRECATED, use redis/ package instead
This file provides backward compatibility.

The Dude S.A.S.

Refactored: 2026-02-09
- redis_infra.py (374 lines) → 6 focused modules
- Better separation of concerns
- Easier testing and maintenance
"""

import logging
logger = logging.getLogger(__name__)

# Import from refactored modules
try:
    from .redis import (
        get_client,
        cache_set,
        cache_get,
        cache_invalidate,
        cache_exists,
        store_session,
        load_session,
        delete_session,
        session_exists,
        publish_event,
        subscribe_to_events,
        increment_counter,
        get_counter,
        reset_counter,
        decrement_counter,
        vadd_record,
        vsim_search,
        get_embedding,
        semantic_cache_get,
        semantic_cache_set
    )
except ImportError:
    # Fallback: define functions inline for backward compatibility
    import os
    import json
    from typing import Any, Optional, Callable
    import redis.asyncio as redis
    import hashlib
    import requests
    
    _redis_client: Optional[redis.Redis] = None
    
    async def get_client() -> redis.Redis:
        """Get or create Redis client singleton."""
        global _redis_client
        if _redis_client is None:
            redis_url = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')
            _redis_client = await redis.from_url(redis_url, decode_responses=True)
            logger.info(f"Redis client created: {redis_url}")
        return _redis_client
    
    async def cache_set(key: str, value: Any, ttl: int = 3600) -> bool:
        """Set a cached value with TTL."""
        try:
            client = await get_client()
            serialized = json.dumps(value)
            await client.setex(key, ttl, serialized)
            logger.info(f"Cached {key} with TTL {ttl}s")
            return True
        except Exception as e:
            logger.error(f"Failed to cache {key}: {str(e)}")
            raise
    
    async def cache_get(key: str) -> Optional[Any]:
        """Get a cached value."""
        try:
            client = await get_client()
            value = await client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Failed to get cache {key}: {str(e)}")
            raise
    
    async def cache_invalidate(pattern: str) -> int:
        """Invalidate all keys matching a pattern."""
        try:
            client = await get_client()
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
        """Check if a key exists in cache."""
        try:
            client = await get_client()
            return await client.exists(key) > 0
        except Exception as e:
            logger.error(f"Failed to check existence of {key}: {str(e)}")
            raise
    
    async def store_session(session_id: str, data: dict, ttl: int = 86400) -> bool:
        """Store session data."""
        try:
            key = f"session:{session_id}"
            return await cache_set(key, data, ttl)
        except Exception as e:
            logger.error(f"Failed to store session {session_id}: {str(e)}")
            raise
    
    async def load_session(session_id: str) -> Optional[dict]:
        """Load session data."""
        try:
            key = f"session:{session_id}"
            return await cache_get(key)
        except Exception as e:
            logger.error(f"Failed to load session {session_id}: {str(e)}")
            raise
    
    async def delete_session(session_id: str) -> bool:
        """Delete a session."""
        try:
            client = await get_client()
            key = f"session:{session_id}"
            await client.delete(key)
            logger.info(f"Deleted session {session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {str(e)}")
            raise
    
    async def publish_event(channel: str, message: dict) -> int:
        """Publish an event to a channel."""
        try:
            client = await get_client()
            serialized = json.dumps(message)
            count = await client.publish(channel, serialized)
            logger.info(f"Published to {channel}: {count} subscribers")
            return count
        except Exception as e:
            logger.error(f"Failed to publish to {channel}: {str(e)}")
            raise
    
    async def subscribe_to_events(channel: str, callback: Callable[[dict], None]) -> None:
        """Subscribe to events on a channel."""
        try:
            client = await get_client()
            pubsub = client.pubsub()
            await pubsub.subscribe(channel)
            logger.info(f"Subscribed to {channel}")
            async for message in pubsub.listen():
                if message['type'] == 'message':
                    data = json.loads(message['data'])
                    callback(data)
        except Exception as e:
            logger.error(f"Failed to subscribe to {channel}: {str(e)}")
            raise
    
    async def increment_counter(key: str, amount: int = 1) -> int:
        """Increment a counter."""
        try:
            client = await get_client()
            value = await client.incrby(key, amount)
            logger.debug(f"Incremented {key} by {amount} to {value}")
            return value
        except Exception as e:
            logger.error(f"Failed to increment {key}: {str(e)}")
            raise
    
    async def get_counter(key: str) -> int:
        """Get current counter value."""
        try:
            client = await get_client()
            value = await client.get(key)
            return int(value) if value else 0
        except Exception as e:
            logger.error(f"Failed to get counter {key}: {str(e)}")
            raise
    
    async def reset_counter(key: str) -> bool:
        """Reset a counter to 0."""
        try:
            client = await get_client()
            await client.set(key, 0)
            logger.info(f"Reset counter {key}")
            return True
        except Exception as e:
            logger.error(f"Failed to reset counter {key}: {str(e)}")
            raise
    
    async def vadd_record(vset_name: str, vector: list, element_id: str) -> bool:
        """Add a vector to a Redis 8 VectorSet."""
        try:
            client = await get_client()
            await client.vset().vadd(vset_name, vector, element_id)
            return True
        except Exception as e:
            logger.error(f"VADD failed: {e}")
            return False
    
    async def vsim_search(vset_name: str, query_vector: list, k: int = 1) -> list:
        """Perform a similarity search in a VectorSet."""
        try:
            client = await get_client()
            results = await client.vset().vsim(vset_name, query_vector, count=k, with_scores=True)
            return results
        except Exception as e:
            logger.error(f"VSIM failed: {e}")
            return []
    
    async def get_embedding(text: str) -> list:
        """Helper to get embeddings from local Ollama."""
        try:
            res = requests.post('http://127.0.0.1:11434/api/embeddings', 
                                json={"model": "nomic-embed-text", "prompt": text},
                                timeout=5)
            if res.status_code == 200:
                return res.json().get('embedding', [])
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
        return []
    
    async def semantic_cache_get(query: str, threshold: float = 0.95) -> Optional[str]:
        """Retrieve semantically similar response from cache."""
        vector = await get_embedding(query)
        if not vector: return None
        
        matches = await vsim_search("semantic_cache", vector, k=1)
        if matches and isinstance(matches, dict):
            for element_id, score in matches.items():
                if score >= threshold:
                    logger.info(f"🚀 Semantic Cache Hit! Score: {score}")
                    return await cache_get(f"response:{element_id}")
        return None
    
    async def semantic_cache_set(query: str, response: str):
        """Store response in semantic cache."""
        query_hash = hashlib.md5(query.encode()).hexdigest()
        vector = await get_embedding(query)
        if not vector: return
        await vadd_record("semantic_cache", vector, query_hash)
        await cache_set(f"response:{query_hash}", response, ttl=86400 * 7)
        logger.info(f"✅ Cached query semantically: {query[:50]}...")

# Additional functions for backward compatibility
async def session_exists(session_id: str) -> bool:
    """Check if a session exists."""
    key = f"session:{session_id}"
    return await cache_exists(key)

async def decrement_counter(key: str, amount: int = 1) -> int:
    """Decrement a counter."""
    try:
        client = await get_client()
        value = await client.incrby(key, -amount)
        return value
    except Exception as e:
        logger.error(f"Failed to decrement {key}: {str(e)}")
        raise
