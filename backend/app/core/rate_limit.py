import redis.asyncio as redis
from fastapi import Request, HTTPException, status

from app.core.config import settings

# Initialize Redis client asynchronously
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def rate_limiter(request: Request):
    """
    Asynchronous Redis-based rate limiting dependency.
    Limits client requests to 60 requests per minute per endpoint.
    """
    client_ip = request.client.host if request.client else "unknown"
    endpoint = request.url.path
    key = f"rate_limit:{endpoint}:{client_ip}"
    
    limit = 60
    window = 60
    
    try:
        current = await redis_client.get(key)
        if current and int(current) >= limit:
            from app.core.metrics import increment_rate_limit_trips
            increment_rate_limit_trips()
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please wait before trying again.",
            )
            
        # Increment and set TTL atomically
        async with redis_client.pipeline(transaction=True) as pipe:
            await pipe.incr(key)
            await pipe.expire(key, window)
            await pipe.execute()
            
    except redis.RedisError as e:
        # Fail open in case Redis is down in local development, but log it
        print(f"Redis rate limiting error: {e}")
        return
