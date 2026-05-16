from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
import enum

class RoleEnum(str, enum.Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'

class StatusEnum(str, enum.Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

class ExpenseBase(BaseModel):
    user_name: str = Field(..., max_length=100)
    user_email: str = Field(..., max_length=100)
    role: RoleEnum
    category: str = Field(..., max_length=100)
    title: str = Field(..., max_length=150)
    description: Optional[str] = None
    amount: float
    expense_date: date

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    status: Optional[StatusEnum] = None
    rejection_reason: Optional[str] = None
    approved_by: Optional[str] = None
    approved_date: Optional[datetime] = None

class ExpenseResponse(ExpenseBase):
    expense_id: int
    status: StatusEnum
    rejection_reason: Optional[str] = None
    approved_by: Optional[str] = None
    approved_date: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
