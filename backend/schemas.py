from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models import UserRole, ExpenseStatus

# ══════════════════════════════════════════
#           REGISTER / AUTH SCHEMAS
# ══════════════════════════════════════════

class RegisterRequest(BaseModel):
    employee_name  : str
    employee_email : EmailStr
    password       : str
    role           : UserRole = UserRole.employee

class LoginRequest(BaseModel):
    employee_email : EmailStr
    password       : str

class Token(BaseModel):
    access_token : str
    token_type   : str = "bearer"

class TokenData(BaseModel):
    employee_email : Optional[str] = None
    role           : Optional[str] = None

# ══════════════════════════════════════════
#            EXPENSE SCHEMAS
# ══════════════════════════════════════════

class ExpenseCreate(BaseModel):
    title          : str
    amount         : float
    description    : Optional[str] = None
    category       : Optional[str] = None

class ExpenseUpdate(BaseModel):
    title          : Optional[str]   = None
    amount         : Optional[float] = None
    description    : Optional[str]   = None
    category       : Optional[str]   = None

class ExpenseResponse(BaseModel):
    id               : int
    employee_name    : str
    employee_email   : str
    role             : UserRole
    title            : str
    amount           : float
    description      : Optional[str]
    category         : Optional[str]
    status           : ExpenseStatus
    reviewer_name    : Optional[str]
    reviewer_email   : Optional[str]
    reviewer_comment : Optional[str]
    created_at       : datetime
    updated_at       : Optional[datetime]

    class Config:
        from_attributes = True

# ══════════════════════════════════════════
#          APPROVAL ACTION SCHEMA
# ══════════════════════════════════════════

class ApprovalAction(BaseModel):
    comment : Optional[str] = None
