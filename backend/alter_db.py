import sqlalchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()
engine = sqlalchemy.create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE expenses ADD COLUMN title VARCHAR(255) DEFAULT 'Expense Request'"))
        conn.commit()
        print("Column 'title' added successfully!")
    except Exception as e:
        print(f"Error (column might already exist): {e}")
