from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from sqlalchemy import text
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    description: str = ""
# removed models and schemas import
from utils.auth import get_current_user, require_role

router = APIRouter(prefix="/categories", tags=["Categories"])

# ─── Get All Categories ───────────────────────────────────────
@router.get("/")
def get_all_categories(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result = db.execute(text("SELECT * FROM categories")).mappings().all()
    return [dict(row) for row in result]

# ─── Create Category ──────────────────────────────────────────
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    name = payload.name
    description = payload.description
    
    existing = db.execute(
        text("SELECT * FROM categories WHERE name = :name"),
        {"name": name}
    ).fetchone()
    
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    db.execute(
        text("INSERT INTO categories (name, description) VALUES (:name, :description)"),
        {"name": name, "description": description}
    )
    db.commit()
    
    new_cat = db.execute(
        text("SELECT * FROM categories WHERE name = :name"),
        {"name": name}
    ).mappings().first()
    
    return dict(new_cat) if new_cat else {}

# ─── Update Category ──────────────────────────────────────────
@router.put("/{category_id}")
def update_category(
    category_id: int,
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    category = db.execute(text("SELECT * FROM categories WHERE id = :id"), {"id": category_id}).mappings().first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    name = payload.name
    description = payload.description
    
    db.execute(
        text("UPDATE categories SET name = :name, description = :description WHERE id = :id"),
        {"name": name, "description": description, "id": category_id}
    )
    db.commit()
    
    updated_cat = db.execute(text("SELECT * FROM categories WHERE id = :id"), {"id": category_id}).mappings().first()
    return dict(updated_cat)

# ─── Delete Category ──────────────────────────────────────────
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    category = db.execute(text("SELECT * FROM categories WHERE id = :id"), {"id": category_id}).mappings().first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    db.execute(text("DELETE FROM categories WHERE id = :id"), {"id": category_id})
    db.commit()
    return {"message": "Category deleted successfully"}
