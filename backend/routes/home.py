from fastapi import APIRouter
from sqlalchemy import create_engine
from schema import CARDS
from dotenv import load_dotenv
import os
# from backend.db import 
load_dotenv()

router = APIRouter()


@router.get("/all_cards",response_model=CARDS)
def all_cards(skip : int = 0, limit : int = 10):
    return 