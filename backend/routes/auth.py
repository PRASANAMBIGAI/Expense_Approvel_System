from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import text
# removed schemas import
from utils.auth import get_current_user, hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "employee"

router = APIRouter(prefix="/auth", tags=["Auth"])

# ─── Register ─────────────────────────────────────────────────
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    name = payload.name
    email = payload.email
    password = payload.password
    role = payload.role

    if not name or not email or not password:
        raise HTTPException(status_code=400, detail="Missing required fields")

    # Check if user exists
    existing_user = db.execute(
        text("SELECT id FROM users WHERE email = :email"),
        {"email": email}
    ).fetchone()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(password)
    
    db.execute(
        text("INSERT INTO users (name, email, password_hash, role) VALUES (:name, :email, :password_hash, :role)"),
        {"name": name, "email": email, "password_hash": hashed_password, "role": role}
    )
    db.commit()
    
    return {"message": "User registered successfully"}

# ─── Login ────────────────────────────────────────────────────
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.execute(
        text("SELECT * FROM users WHERE email = :email"),
        {"email": form_data.username}
    ).mappings().first()

    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"employee_email": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

# ─── Get Current User ─────────────────────────────────────────
@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    # Remove password hash before returning
    user_data = dict(current_user)
    user_data.pop("password_hash", None)
    return user_data
