from fastapi import APIRouter, Request, Depends
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session
from schema import CARDS
from ..decorator import cache, rate_limit
from database import get_db
from typing import Annotated
router = APIRouter()

@router.get("/cards/{source}/{source_id}")
@rate_limit()
@cache()
async def card(source:str, source_id:str, request: Request, db=Annotated[Session, Depends(get_db)]):
    return