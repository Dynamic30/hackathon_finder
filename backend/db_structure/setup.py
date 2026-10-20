import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

SQL_FILE = Path(__file__).parent / "hacakthon.sql"


def setup_db():
    engine = create_engine(os.getenv("sql_db"))
    with engine.begin() as conn:                     # commits at the end of the block
        conn.exec_driver_sql(SQL_FILE.read_text())
    print("db set up")


if __name__ == "__main__":
    setup_db()
