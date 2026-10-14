from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()



engine = create_engine(os.getenv("sql_db"))

def get_conn():
    with engine.connect() as conn:
        yield conn

# Queries 

_ALL_CARDS = """
    SELECT title, organizer, source, source_url, mode, city, state,
           tags, prize_amount, reg_end_at, image_url, is_paid,
           team_min, team_max
      FROM hackathons
     WHERE is_active
     ORDER BY reg_end_at ASC NULLS LAST
     LIMIT :limit OFFSET :skip
"""


# funcs

def get_all_cards(conn, skip=0, limit=10):
    rows = conn.execute(text(_ALL_CARDS), {"limit": limit, "skip": skip})
    return rows.mappings().all()
