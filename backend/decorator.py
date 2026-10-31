from settings import redis_cache, redis_rate_limiter
import json
from functools import wraps
from fastapi import HTTPException, Request
import hashlib

def cache(expire: int = 120):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Key includes function name + all params (page, limit, filters)
            key_args = {k: v for k, v in kwargs.items() if k not in ("request", "db")}
            raw_key = f"{func.__name__}:{json.dumps(key_args, sort_keys=True, default=str)}"
            key = f"cache:{hashlib.md5(raw_key.encode()).hexdigest()}"

            # Check cache
            cached = await redis_cache.get(key)
            if cached:
                return json.loads(cached)

            # Miss — run actual function
            result = await func(*args, **kwargs)
            await redis_cache.setex(key, expire, json.dumps(result, default=str))
            return result
        return wrapper
    return decorator

def rate_limit(max_requests: int = 120, window: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, request: Request, **kwargs):
            # When auth is added, just set request.state.user
            user = getattr(request.state, "user", None)
            identifier = user.id if user else request.client.host

            key = f"rate:{func.__name__}:{identifier}"

            current = await redis_rate_limiter.incr(key)
            if current == 1:
                await redis_rate_limiter.expire(key, window)

            if current > max_requests:
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Slow down."
                )

            return await func(*args, request=request, **kwargs)
        return wrapper
    return decorator