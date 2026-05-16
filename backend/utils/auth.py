from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import os

# ─── Config ───────────────────────────────────────────────────
SECRET_KEY      = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM       = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ─── Password Hashing ─────────────────────────────────────────
pwd_context     = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme   = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ─── Hash Password ────────────────────────────────────────────
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ─── Verify Password ──────────────────────────────────────────
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ─── Create JWT Token ─────────────────────────────────────────
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire    = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ─── Decode JWT Token ─────────────────────────────────────────
def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# ─── Get Current User (Dependency) ───────────────────────────
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from models import Expense  # single table — identity derived from latest record by email

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    employee_email: str = payload.get("employee_email")
    if employee_email is None:
        raise credentials_exception

    # Fetch any row for this email to get role & name (identity record)
    user = db.query(Expense).filter(Expense.employee_email == employee_email).first()
    if user is None:
        raise credentials_exception

    return user

# ─── Role Guard (Dependency) ──────────────────────────────────
def require_role(*roles: str):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role(s): {list(roles)}"
            )
        return current_user
    return role_checker
