"""
Redis Pub/Sub Operations - The Dude S.A.S.
Event publishing and subscription channels.
"""
import json
import logging
from typing import Callable
import redis.asyncio as redis


logger = logging.getLogger(__name__)


async def publish_event(channel: str, message: dict) -> int:
    """
    Publish an event to a channel.

    Args:
        channel: Channel name
        message: Message dictionary

    Returns:
        Number of subscribers that received the message
    """
    from .redis_client import get_client
    
    try:
        client: redis.Redis = await get_client()
        serialized = json.dumps(message)
        count = await client.publish(channel, serialized)
        logger.info(f"Published to {channel}: {count} subscribers")
        return count
    except Exception as e:
        logger.error(f"Failed to publish to {channel}: {str(e)}")
        raise


async def subscribe_to_events(channel: str, callback: Callable[[dict], None]) -> None:
    """
    Subscribe to events on a channel.

    Args:
        channel: Channel name
        callback: Function to call with each message

    Note:
        This is a blocking operation. Run in a separate task/thread.
    """
    from .redis_client import get_client
    
    try:
        client: redis.Redis = await get_client()
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
