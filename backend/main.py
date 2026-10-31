from fastapi import FastAPI
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from contextlib import asynccontextmanager
from settings import redis_cache, redis_rate_limiter
from routes.home import router as home_router
from routes.cards import router as card_routers
@asynccontextmanager
async def lifespan(app:FastAPI):
    # add redis (cache + rate limiter) and db conn + table set up here

    yield
    await redis_cache.aclose()
    await redis_rate_limiter.aclose()

    return

app = FastAPI(title="Hackathon Finder",lifespan=lifespan)
FRONTEND = Path(__file__).resolve().parent.parent / "frontend"


app.include_router(home_router,prefix="/v1")
app.include_router(card_routers,prefix="/v1")
app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="frontend")   # must be last


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(FRONTEND / "index.html")

@app.exception_handler(404)
async def not_found(request, exc):
    if "text/html" in request.headers.get("accept", ""):          # browser opening a URL
        return FileResponse(FRONTEND / "error.html", status_code=404)
    return JSONResponse({"detail": exc.detail}, status_code=404)   # fetch() / API clients
