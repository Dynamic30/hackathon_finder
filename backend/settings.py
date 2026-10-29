from redis.asyncio import Redis

redis_cache = Redis(host="localhost", port=9746,db=1,decode_responses=True)
redis_rate_limiter = Redis(host="localhost",port=9745,db=1,decode_responses=True)
