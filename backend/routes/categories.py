from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import CategoryCreate, CategoryResponse
from utils.auth import get_current_user, require_role

router = APIRouter(prefix="/categories", tags=["Categories"])

# ─── Get All Categories ───────────────────────────────────────
@router.get("/", response_model=List[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # TODO: fetch and return all categories
    pass

# ─── Create Category ──────────────────────────────────────────
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    # TODO: implement category creation logic
    pass

# ─── Update Category ──────────────────────────────────────────
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    # TODO: implement category update logic
    pass

# ─── Delete Category ──────────────────────────────────────────
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    # TODO: implement category deletion logic
    pass
