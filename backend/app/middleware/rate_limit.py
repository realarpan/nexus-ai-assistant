"""Rate limiting middleware"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.redis_client import get_redis
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.redis = get_redis()
    
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Create rate limit key
        key = f"rate_limit:{client_ip}"
        
        try:
            # Get current request count
            current = self.redis.get(key)
            
            if current is None:
                # First request
                self.redis.setex(key, 60, 1)
            else:
                current = int(current)
                if current >= self.requests_per_minute:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit exceeded. Please try again later."
                    )
                self.redis.incr(key)
        except Exception as e:
            # If Redis fails, allow request
            pass
        
        response = await call_next(request)
        return response