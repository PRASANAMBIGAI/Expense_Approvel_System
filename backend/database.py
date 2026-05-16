from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# ─── Database URL ─────────────────────────────────────────────
# Format: mysql+pymysql://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@localhost:3306/expense_db")

# ─── Engine ───────────────────────────────────────────────────
engine = create_engine(DATABASE_URL)

# ─── Session Factory ──────────────────────────────────────────
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ─── Base Class for Models ────────────────────────────────────
Base = declarative_base()

# ─── Dependency: DB Session per Request ───────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
