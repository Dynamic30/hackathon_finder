from redis.asyncio import Redis
import os
from dotenv import load_dotenv

load_dotenv()


redis_cache = Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
redis_rate_limiter = Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
