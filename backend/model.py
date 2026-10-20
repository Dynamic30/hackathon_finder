from __future__ import annotations
from datetime import datetime

from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Hackathon(Base):
    __tablename__ = "hackathons"

    id: Mapped[int] = mapped_column(primary_key=True)

    source: Mapped[str]
    source_id: Mapped[str]
    source_url: Mapped[str]
    scraped_at: Mapped[datetime]

    title: Mapped[str]
    organizer: Mapped[str | None]
    description: Mapped[str | None]
    description_format: Mapped[str | None]

    start_at: Mapped[datetime | None]
    end_at: Mapped[datetime | None]
    reg_start_at: Mapped[datetime | None]
    reg_end_at: Mapped[datetime | None]
    date_confidence: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    mode: Mapped[str]
    city: Mapped[str | None]
    state: Mapped[str | None]
    country: Mapped[str | None]
    location_raw: Mapped[str | None]

    prize_amount: Mapped[int | None]
    prize_currency: Mapped[str | None]
    prize_is_total: Mapped[bool | None]

    team_min: Mapped[int | None]
    team_max: Mapped[int | None]
    registrations: Mapped[int | None]
    is_paid: Mapped[bool | None]

    tags: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list)
    image_url: Mapped[str | None]
    # raw: Mapped[dict] = mapped_column(JSONB)
