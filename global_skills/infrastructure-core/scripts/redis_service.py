"""
Redis Service - The Dude S.A.S.
Centralized Redis client with connection pooling and async support.
"""
from functools import lru_cache
from typing import Any, Optional, Union
import redis
from redis.asyncio import Redis as AsyncRedis
from ..config import get_config


class RedisService:
    """Redis service with connection pooling"""
    
    _instance: Optional["RedisService"] = None
    _sync_client: Optional[redis.Redis] = None
    _async_client: Optional[AsyncRedis] = None
    
    def __new__(cls) -> "RedisService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._sync_client is not None:
            return
            
        config = get_config()
        self._sync_client = redis.Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            password=config.redis.password if config.redis.password else None,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
            max_connections=20
        )
        
        self._async_client = AsyncRedis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            password=config.redis.password if config.redis.password else None,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
            max_connections=20
        )
    
    @property
    def sync_client(self) -> redis.Redis:
        """Get synchronous Redis client"""
        if self._sync_client is None:
            self.__init__()
        return self._sync_client
    
    @property
    def async_client(self) -> AsyncRedis:
        """Get asynchronous Redis client"""
        if self._async_client is None:
            self.__init__()
        return self._async_client
    
    def get(self, key: str) -> Optional[str]:
        """Get value from Redis"""
        try:
            return self.sync_client.get(key)
        except redis.ConnectionError:
            return None
    
    def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        """Set value in Redis"""
        try:
            self.sync_client.set(key, value, ex=ex)
            return True
        except redis.ConnectionError:
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        try:
            self.sync_client.delete(key)
            return True
        except redis.ConnectionError:
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        try:
            return self.sync_client.exists(key) > 0
        except redis.ConnectionError:
            return False
    
    def keys(self, pattern: str = "*") -> list:
        """Get keys matching pattern"""
        try:
            return self.sync_client.keys(pattern)
        except redis.ConnectionError:
            return []
    
    def flushdb(self) -> bool:
        """Flush current database"""
        try:
            self.sync_client.flushdb()
            return True
        except redis.ConnectionError:
            return False
    
    def ping(self) -> bool:
        """Check Redis connection"""
        try:
            return self.sync_client.ping()
        except redis.ConnectionError:
            return False


@lru_cache(maxsize=1)
def get_redis() -> RedisService:
    """Get Redis service singleton (cached)"""
    return RedisService()


async def cache_get(key: str) -> Optional[str]:
    """Async cache get function (for backward compatibility)"""
    service = get_redis()
    return service.get(key)


async def cache_set(key: str, value: str, ex: Optional[int] = None) -> bool:
    """Async cache set function (for backward compatibility)"""
    service = get_redis()
    return service.set(key, value, ex)


class LeadStateManager:
    """Manage lead state in Redis"""
    
    def __init__(self):
        self.redis = get_redis()
    
    async def get_state(self, lead_id: str) -> Optional[str]:
        """Get lead state"""
        return await cache_get(f"lead_state:{lead_id}")
    
    async def set_state(self, lead_id: str, state: str, ex: int = 3600) -> bool:
        """Set lead state (default 1 hour expiration)"""
        return await cache_set(f"lead_state:{lead_id}", state, ex=ex)
    
    async def is_active_conversation(self, lead_id: str) -> bool:
        """Check if lead has active conversation"""
        state = await self.get_state(lead_id)
        return state and state not in ["ICEBREAKER", "COLD_GHOST"]
    
    def get_sync_state(self, lead_id: str) -> Optional[str]:
        """Get lead state (sync)"""
        return self.redis.get(f"lead_state:{lead_id}")
    
    def set_sync_state(self, lead_id: str, state: str, ex: int = 3600) -> bool:
        """Set lead state (sync)"""
        return self.redis.set(f"lead_state:{lead_id}", state, ex=ex)
