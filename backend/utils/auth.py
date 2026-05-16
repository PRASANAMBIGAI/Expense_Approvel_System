import bcrypt
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

oauth2_scheme   = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ─── Hash Password ────────────────────────────────────────────
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# ─── Verify Password ──────────────────────────────────────────
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

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
    from sqlalchemy import text
    
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

    # Fetch user identity
    result = db.execute(
        text("SELECT * FROM users WHERE email = :email LIMIT 1"),
        {"email": employee_email}
    ).mappings().first()
    
    if result is None:
        raise credentials_exception

    return dict(result)

# ─── Role Guard (Dependency) ──────────────────────────────────
def require_role(*roles: str):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.get("role") not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role(s): {list(roles)}"
            )
        return current_user
    return role_checker
