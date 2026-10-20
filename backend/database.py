from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()

sql_db = os.getenv("sql_db")

engine = create_engine(sql_db)

SessionLocal = sessionmaker(autoflush=False, bind=engine, autocommit=False)

class Base(DeclarativeBase): 
    pass

def get_db():
    with SessionLocal() as db:
        yield db

