from pydantic import BaseModel
from datetime import datetime, timezone
import asyncio
# from scrapers.hack2skills import

class DB_STRUCTURE(BaseModel):
    source: str
    source_id: int
    source_url: str
    scraped_at: datetime

    title: str
    organizer: None
    description: None
    description_format: None

    start_at: str
    end_at: str
    reg_start_at: str
    reg_end_at: str
    date_confidence: str

    mode: str 
    city: str
    state: str
    country: str
    location_raw: str

    prize_amount: int
    prize_currency: str
    prize_is_total: int

    team_min: int | str
    team_max: int
    registrations:str
    is_paid: bool

    tags: str
    image_url: str

    raw: dict
    


def db_push():
    return

async def main():
    return
