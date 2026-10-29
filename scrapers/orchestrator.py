from pydantic import BaseModel
from datetime import datetime, timezone
import asyncio
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from scrapers import unstop,hackerearth,devpost,devfolio,hack2skills
import json
import os

load_dotenv()

sql_db = os.getenv("sql_db")

engine = create_engine(sql_db)
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

    # raw: dict


async def scraper_runs():
    return await asyncio.gather(
        asyncio.to_thread(unstop.unstop_data),
        asyncio.to_thread(hackerearth.hackerearth_data),
        asyncio.to_thread(devfolio.devfolio_data),
        asyncio.to_thread(devpost.devpost_data),
        asyncio.to_thread(hack2skills.hack2skill_data),
        return_exceptions=True,
    )

async def main_orchestrator():
    from backend.db_structure.setup import setup_db
    await asyncio.to_thread(setup_db)                # safe to repeat, SQL is IF NOT EXISTS

    scraped_data = await scraper_runs()
    await asyncio.to_thread(db_format_push, scraped_data)


# main function to push data to db
def db_format_push(scraped_data):
    """
    compare the scraped data with what db has and set is_active = false for existing ones which:
        1. have date expiry
        2. are not in the current scraped data
    # TODO: re-compute priority
    """
    now = datetime.now(timezone.utc)

    # flatten + validate, skip scrapers that failed
    items = [DB_STRUCTURE(**i) for r in scraped_data if not isinstance(r, Exception) for i in r]
    ok_sources = {i.source for i in items}   # sources that returned data

    # map of everything already in the db, keyed by (source, source_id)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, source, source_id, start_at, end_at, reg_start_at, reg_end_at FROM hackathons"
        )).mappings().all()
        existing = {(r["source"], r["source_id"]): r for r in rows}

    new, to_check = [], []
    scraped_keys = set()
    for item in items:
        key = (item.source, item.source_id)
        scraped_keys.add(key)
        if key not in existing:
            new.append(item)
        else:
            to_check.append(item)

    def is_expired(end):
        if end.tzinfo is None:                       # db timestamps may be naive
            end = end.replace(tzinfo=timezone.utc)
        return now > end

    deactivate, set_active = [], []                  # db ids

    # in db and scraped -> check dates (scraped first, then db; reg end before end)
    for item in to_check:
        row = existing[(item.source, item.source_id)]
        end = item.reg_end_at or item.end_at or row["reg_end_at"] or row["end_at"]
        if end is None:
            continue                                 # no dates anywhere -> leave as is
        (deactivate if is_expired(end) else set_active).append(row["id"])

    # in db but not scraped -> inactive (only for sources that returned data)
    for key, row in existing.items():
        if key[0] in ok_sources and key not in scraped_keys:
            deactivate.append(row["id"])
    # new hackathons: set is_active from their own dates, then insert
    for item in new:
        end = item.reg_end_at or item.end_at
        if end and is_expired(end):
            item.is_active = False

    with engine.begin() as conn:                     # commits at the end of the block
        if new:
            data = [i.model_dump() for i in new]
            cols = list(data[0])
            conn.execute(text(
                f"INSERT INTO hackathons ({', '.join(cols)}) "
                f"VALUES ({', '.join(':' + c for c in cols)})"
            ), data)

        if deactivate:
            conn.execute(text("UPDATE hackathons SET is_active = FALSE WHERE id = ANY(:ids)"), {"ids": deactivate})
        if set_active:
            conn.execute(text("UPDATE hackathons SET is_active = TRUE WHERE id = ANY(:ids)"), {"ids": set_active})



if __name__ == "__main__":
    asyncio.run(main_orchestrator())
    # data = asyncio.run(scraper_runs())
    # with open("tests/orchestrator_test.json",'w') as file:
        # json.dump(data,file,indent=2,default=str)