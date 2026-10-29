from fastapi import FastAPI
from contextlib import asynccontextmanager
from settings import redis_cache, redis_rate_limiter
from routes.home import router as home_router
@asynccontextmanager
async def lifespan(app:FastAPI):
    # add redis (cache + rate limiter) and db conn + table set up here

    yield
    await redis_cache.aclose()
    await redis_rate_limiter.aclose()

    return

app = FastAPI(title="Hackathon Finder",lifespan=lifespan)

app.include_router(home_router,prefix="/v1")