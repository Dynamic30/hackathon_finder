from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session
from schema import CARDS, HackathonDetail
from decorator import cache, rate_limit
from database import get_db
from typing import Annotated
from model import Hackathon

router = APIRouter()

@router.get("/cards/{source}/{source_id}",response_model=HackathonDetail)
@rate_limit()
async def card(source:str, source_id:str, request: Request, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Hackathon).where(Hackathon.source == source,Hackathon.source_id == source_id)).scalar_one_or_none()
    if not result:
        raise HTTPException(404, "Hackathon Not Found")
    return result