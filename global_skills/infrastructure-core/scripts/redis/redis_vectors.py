"""
Redis Vector Operations - The Dude S.A.S.
Vector similarity search and semantic caching using Redis 8 VectorSet.
"""
import json
import logging
import hashlib
import requests
from typing import Optional
import redis.asyncio as redis


logger = logging.getLogger(__name__)


async def vadd_record(vset_name: str, vector: list, element_id: str) -> bool:
    """
    Add a vector to a Redis 8 VectorSet.
    
    Args:
        vset_name: Name of the VectorSet.
        vector: List of floats.
        element_id: Identifier for the element.
    """
    from .redis_client import get_client
    
    try:
        client: redis.Redis = await get_client()
        # VADD <key> VALUES <dim> <v1> <v2> ... <vn> <element_id>
        await client.vset().vadd(vset_name, vector, element_id)
        logger.debug(f"Added vector to {vset_name}: {element_id}")
        return True
    except Exception as e:
        logger.error(f"VADD failed for {vset_name}: {e}")
        return False


async def vsim_search(vset_name: str, query_vector: list, k: int = 1) -> list:
    """
    Perform a similarity search in a VectorSet.
    
    Args:
        vset_name: Name of the VectorSet.
        query_vector: Query vector.
        k: Number of results to return.
    
    Returns:
        List of [id, score] results.
    """
    from .redis_client import get_client
    
    try:
        client: redis.Redis = await get_client()
        results = await client.vset().vsim(vset_name, query_vector, count=k, with_scores=True)
        return results
    except Exception as e:
        logger.error(f"VSIM failed for {vset_name}: {e}")
        return []


async def get_embedding(text: str) -> list:
    """
    Helper to get embeddings from local Ollama (nomic-embed-text).
    
    Args:
        text: Text to embed.
    
    Returns:
        List of floats representing the embedding.
    """
    try:
        res = requests.post(
            'http://127.0.0.1:11434/api/embeddings',
            json={"model": "nomic-embed-text", "prompt": text},
            timeout=5
        )
        if res.status_code == 200:
            return res.json().get('embedding', [])
    except Exception as e:
        logger.error(f"Ollama embedding failed: {e}")
    return []


async def semantic_cache_get(query: str, threshold: float = 0.95) -> Optional[str]:
    """
    Retrieve semantically similar response from cache.
    
    Args:
        query: Query text.
        threshold: Similarity threshold (0-1).
    
    Returns:
        Cached response or None.
    """
    from .redis_cache import cache_get
    
    vector = await get_embedding(query)
    if not vector:
        return None
    
    matches = await vsim_search("semantic_cache", vector, k=1)
    if matches and isinstance(matches, dict):
        # Redis 8 dictionary response: {id: score}
        for element_id, score in matches.items():
            if score >= threshold:
                logger.info(f"🚀 Semantic Cache Hit! Score: {score}")
                return await cache_get(f"response:{element_id}")
    return None


async def semantic_cache_set(query: str, response: str, ttl: int = 604800) -> bool:
    """
    Store response in semantic cache.
    
    Args:
        query: Query text.
        response: Response to cache.
        ttl: TTL in seconds (default: 7 days).
    
    Returns:
        True if cached successfully.
    """
    from .redis_cache import cache_set
    
    vector = await get_embedding(query)
    if not vector:
        return False
    
    query_hash = hashlib.md5(query.encode()).hexdigest()
    # Store the vector
    await vadd_record("semantic_cache", vector, query_hash)
    # Store the actual response string
    await cache_set(f"response:{query_hash}", response, ttl=ttl)
    logger.info(f"✅ Cached query semantically: {query[:50]}...")
    return True
