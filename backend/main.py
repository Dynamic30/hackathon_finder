from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app:FastAPI):
    # add redis (cache + rate limiter) and db conn + table set up here
    return

app = FastAPI(title="Hackathon Finder")
