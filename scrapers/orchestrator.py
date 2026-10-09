from pydantic import BaseModel
from datetime import datetime, timezone
import asyncio
import sqlalchemy as db
from scrapers import unstop,hackerearth,devpost,devfolio,hack2skills
import json
# engine = db.create_engine()

# add logger in v2

class DB_STRUCTURE(BaseModel):
    source: str
    source_id: str
    source_url: str
    scraped_at: datetime

    title: str
    organizer: str | None = None
    description: str | None = None
    description_format: str | None = None

    start_at: datetime | None = None
    end_at: datetime | None = None
    reg_start_at: datetime | None = None
    reg_end_at: datetime | None = None
    date_confidence: str
    is_active: bool = True

    mode: str
    city: str | None = None
    state: str | None = None
    country: str | None = None
    location_raw: str | None = None

    prize_amount: int | None = None
    prize_currency: str | None = None
    prize_is_total: bool | None = None

    team_min: int | None = None
    team_max: int | None = None
    registrations: int | None = None
    is_paid: bool | None = None

    tags: list[str] = []
    image_url: str | None = None

    raw: dict



def db_push():
    return

async def scraper_runs():
    return await asyncio.gather(
        asyncio.to_thread(unstop.unstop_data),
        asyncio.to_thread(hackerearth.hackerearth_data),
        asyncio.to_thread(devfolio.devfolio_data),
        asyncio.to_thread(devpost.devpost_data),
        asyncio.to_thread(hack2skills.hack2skill_data),
        return_exceptions=True,
    )



async def current_status_update():
    return

if __name__ == "__main__":
    print(db.__version__)
    data = asyncio.run(scraper_runs())
    with open("tests/orchestrator_test.json",'w') as file:
        json.dump(data,file,indent=2)