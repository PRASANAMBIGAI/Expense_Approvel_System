from sqlalchemy import Column, Integer, String, Enum, Text, Numeric, Date, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class RoleEnum(str, enum.Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'

class StatusEnum(str, enum.Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

class Expense(Base):
    __tablename__ = 'expenses'

    expense_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(100), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    category = Column(String(100), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    expense_date = Column(Date, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    rejection_reason = Column(Text, nullable=True)
    approved_by = Column(String(100), nullable=True)
    approved_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
