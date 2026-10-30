from fastapi import APIRouter, Request, Depends
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, load_only
from schema import CARDS, PriorityCard
from dotenv import load_dotenv
from decorator import cache, rate_limit
from typing import Annotated, Literal
from database import get_db
from model import Hackathon
from datetime import datetime, timezone


# from backend.db import 
router = APIRouter()




def priority(all_hackathons):

    CURRENCY_TO_INR = {None: 1, "INR": 1, "USD": 88, "EUR": 96, "GBP": 112, "CAD": 64, "AUD": 58, "MXN": 4.8}

    scored_hackathons = []

    for hackathon in all_hackathons:
        # urgency: how close the registration deadline is (0-55)
        deadline = hackathon.reg_end_at or hackathon.end_at
        if deadline is None:
            urgency_score = 14
        else:
            if deadline.tzinfo is None:
                deadline = deadline.replace(tzinfo=timezone.utc)
            days_left = (deadline - datetime.now(timezone.utc)).days
            date_is_reliable = hackathon.date_confidence in ("exact", "parsed")
            if days_left < 0:
                urgency_score = 0
            elif days_left <= 3:
                urgency_score = 55 if date_is_reliable else 33
            elif days_left <= 7:
                urgency_score = 44
            elif days_left <= 14:
                urgency_score = 33
            elif days_left <= 30:
                urgency_score = 19
            else:
                urgency_score = 8

        # prize: cash value, normalized to INR so currencies compare (0-35)
        prize_in_inr = (hackathon.prize_amount or 0) * CURRENCY_TO_INR.get(hackathon.prize_currency, 1)
        if prize_in_inr >= 500000:
            prize_score = 35
        elif prize_in_inr >= 100000:
            prize_score = 28
        elif prize_in_inr >= 25000:
            prize_score = 19
        elif prize_in_inr >= 5000:
            prize_score = 10
        elif prize_in_inr > 0:
            prize_score = 5
        else:
            prize_score = 0

        # popularity: how many have registered, used as a tiebreaker (0-10)
        registrations = hackathon.registrations or 0
        if registrations >= 5000:
            popularity_score = 10
        elif registrations >= 1000:
            popularity_score = 7
        elif registrations >= 200:
            popularity_score = 4
        elif registrations >= 20:
            popularity_score = 2
        else:
            popularity_score = 0

        total_score = urgency_score + prize_score + popularity_score
        tier = "high" if total_score >= 60 else "medium" if total_score >= 35 else "low"

        hackathon.priority_score = total_score
        hackathon.priority_tier = tier
        scored_hackathons.append(hackathon)

    scored_hackathons.sort(key=lambda hackathon: hackathon.priority_score, reverse=True)
    return scored_hackathons


@router.get("/all_cards", response_model=list[CARDS])
@rate_limit()
@cache()
async def all_cards(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    sort_by: Literal["Prize", "Urgency", "Recent", "Priority"] = "Priority",
    tier: Literal["high", "medium", "low"] | None = None,
    status: Literal["active", "inactive", "all"] = "active",
    skip: int = 0,
    limit: int = 10,
):

    query = select(Hackathon).options(
        load_only(
            Hackathon.id, Hackathon.title, Hackathon.source, Hackathon.source_url,
            Hackathon.organizer, Hackathon.mode, Hackathon.tags, Hackathon.is_paid,
            Hackathon.team_min, Hackathon.team_max,
            Hackathon.city, Hackathon.state, Hackathon.country, Hackathon.location_raw,
            Hackathon.prize_amount, Hackathon.prize_currency,
            Hackathon.reg_end_at, Hackathon.end_at,
            Hackathon.date_confidence, Hackathon.registrations,
            Hackathon.is_active, Hackathon.scraped_at,
        )
    ).order_by(Hackathon.id)

    if status == "active":
        query = query.where(Hackathon.is_active)
    elif status == "inactive":
        query = query.where(~Hackathon.is_active)
    # "all" → no filter

    all_hackathons = db.execute(query).scalars().all()
    ranked = priority(all_hackathons)

    if tier is not None:
        ranked = [hackathon for hackathon in ranked if hackathon.priority_tier == tier]

    if sort_by == "Prize":
        ranked.sort(key=lambda hackathon: hackathon.prize_amount or 0, reverse=True)
    elif sort_by == "Urgency":
        ranked.sort(key=lambda hackathon: hackathon.reg_end_at or hackathon.end_at or datetime.max.replace(tzinfo=timezone.utc))
    elif sort_by == "Recent":
        ranked.sort(key=lambda hackathon: hackathon.scraped_at, reverse=True)

    page = ranked[skip : skip + limit]
    return [CARDS.model_validate(hackathon, from_attributes=True).model_dump(mode="json") for hackathon in page]

