from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import RegisterRequest, ExpenseResponse, LoginRequest, Token
from utils.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

# ─── Register ─────────────────────────────────────────────────
@router.post("/register", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    # TODO: implement registration logic
    pass

# ─── Login ────────────────────────────────────────────────────
@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    # TODO: implement login & token generation logic
    pass

# ─── Get Current User ─────────────────────────────────────────
@router.get("/me", response_model=ExpenseResponse)
def get_me(current_user=Depends(get_current_user)):
    # TODO: return current logged-in user
    return current_user
