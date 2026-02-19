"""
Redis Infrastructure - The Dude S.A.S.
Modularized Redis operations with async support.
Provides backward compatibility with redis_infra.py.
"""

# Client management
from .redis_client import get_client

# Cache operations
from .redis_cache import (
    cache_set,
    cache_get,
    cache_invalidate,
    cache_exists
)

# Session management
from .redis_session import (
    store_session,
    load_session,
    delete_session,
    session_exists
)

# Pub/Sub operations
from .redis_pubsub import (
    publish_event,
    subscribe_to_events
)

# Counter operations
from .redis_counter import (
    increment_counter,
    get_counter,
    reset_counter,
    decrement_counter
)

# Vector operations
from .redis_vectors import (
    vadd_record,
    vsim_search,
    get_embedding,
    semantic_cache_get,
    semantic_cache_set
)

__all__ = [
    # Client
    "get_client",
    
    # Cache
    "cache_set",
    "cache_get",
    "cache_invalidate",
    "cache_exists",
    
    # Session
    "store_session",
    "load_session",
    "delete_session",
    "session_exists",
    
    # Pub/Sub
    "publish_event",
    "subscribe_to_events",
    
    # Counter
    "increment_counter",
    "get_counter",
    "reset_counter",
    "decrement_counter",
    
    # Vectors
    "vadd_record",
    "vsim_search",
    "get_embedding",
    "semantic_cache_get",
    "semantic_cache_set",
]
