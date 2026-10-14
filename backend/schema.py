from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class Mode(str, Enum):          # you imported Enum but haven't used it
    online = "online"
    offline = "offline"
    hybrid = "hybrid"
    unknown = "unknown"


class CARDS(BaseModel):
    source: str
    source_url: str
    title: str
    mode: Mode
    location: str | None = None
    tags: list[str] = []
    start_at: datetime | None = None
    reg_end_at: datetime | None = None
    prize_amount: int | None = None
    image_url: str | None = None
    organizer: str | None = None
    is_paid: bool | None = None
    team_min: int | None = None
    team_max: int | None = None

