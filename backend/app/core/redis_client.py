"""Redis client configuration"""

import redis
from app.core.config import settings

redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_keepalive=True
)

def get_redis():
    """Gets Redis client"""
    return redis_client