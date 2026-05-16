from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from database import Base
import enum

# ─── Role Enum ────────────────────────────────────────────────
class UserRole(str, enum.Enum):
    employee = "employee"
    manager  = "manager"
    admin    = "admin"

# ─── Status Enum ──────────────────────────────────────────────
class ExpenseStatus(str, enum.Enum):
    pending  = "pending"
    approved = "approved"
    rejected = "rejected"

# ─── Single Expense Table ─────────────────────────────────────
class Expense(Base):
    __tablename__ = "expenses"

    id               = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # ── Employee Info ───────────────────────────────────────────
    employee_name    = Column(String(100), nullable=False)
    employee_email   = Column(String(150), nullable=False, index=True)
    hashed_password  = Column(String(255), nullable=False)
    role             = Column(Enum(UserRole), default=UserRole.employee, nullable=False)

    # ── Expense Details ─────────────────────────────────────────
    title            = Column(String(200), nullable=False)
    amount           = Column(Float, nullable=False)
    description      = Column(String(500), nullable=True)
    category         = Column(String(100), nullable=True)   # plain string, no FK

    # ── Approval Info ───────────────────────────────────────────
    status           = Column(Enum(ExpenseStatus), default=ExpenseStatus.pending, nullable=False)
    reviewer_name    = Column(String(100), nullable=True)
    reviewer_email   = Column(String(150), nullable=True)
    reviewer_comment = Column(String(500), nullable=True)

    # ── Timestamps ──────────────────────────────────────────────
    created_at       = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at       = Column(DateTime, onupdate=func.now(), nullable=True)
