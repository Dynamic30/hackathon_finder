# contain pydantic schema for api calls

from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime

class Mode(str, Enum):          # you imported Enum but haven't used it
    online = "online"
    offline = "offline"
    hybrid = "hybrid"
    unknown = "unknown"


class CARDS(BaseModel):
    id: int
    source: str
    source_url: str
    title: str
    organizer: str | None = None
    mode: Mode
    tags: list[str] = []
    is_paid: bool | None = None
    team_min: int | None = None
    team_max: int | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    location_raw: str | None = None
    prize_amount: int | None = None
    prize_currency: str | None = None
    reg_end_at: datetime | None = None
    end_at: datetime | None = None
    priority_tier: str          # set by priority()

class HackathonDetail(CARDS):
    description: str | None = None
    description_format: str | None = None
    start_at: datetime | None = None
    reg_start_at: datetime | None = None
    registrations: int | None = None
    image_url: str | None = None
    location_raw: str | None = None   # already in CARDS, can be removed


class PriorityCard(CARDS):
    priority_score: int
    priority_tier: str
    model_config = ConfigDict(from_attributes=True)


