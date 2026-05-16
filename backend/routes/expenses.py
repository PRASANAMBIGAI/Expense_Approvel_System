from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import text
from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category_id: int
    description: str = ""
from sqlalchemy.orm import Session
from typing import List
from database import get_db
# removed schemas import
from utils.auth import get_current_user, require_role

router = APIRouter(prefix="/expenses", tags=["Expenses"])

# ─── Submit Expense ───────────────────────────────────────────
@router.post("/", status_code=status.HTTP_201_CREATED)
def submit_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    title = payload.title
    amount = payload.amount
    category_id = payload.category_id
    description = payload.description
    
    if amount is None or category_id is None or not title:
        raise HTTPException(status_code=400, detail="title, amount and category_id are required")
        
    db.execute(
        text("INSERT INTO expenses (user_id, category_id, amount, description, title) VALUES (:user_id, :category_id, :amount, :description, :title)"),
        {"user_id": current_user["id"], "category_id": category_id, "amount": amount, "description": description, "title": title}
    )
    db.commit()
    
    new_expense = db.execute(
        text("SELECT * FROM expenses WHERE user_id = :user_id ORDER BY id DESC LIMIT 1"),
        {"user_id": current_user["id"]}
    ).mappings().first()
    
    return dict(new_expense)

# ─── Get All Expenses ─────────────────────────────────────────
@router.get("/")
def get_expenses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = """
        SELECT e.*, c.name as category, u.name as employee_name
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.id
        LEFT JOIN users u ON e.user_id = u.id
    """
    if current_user.get("role") in ["manager", "admin"]:
        result = db.execute(text(query + " ORDER BY e.created_at DESC")).mappings().all()
    else:
        result = db.execute(text(query + " WHERE e.user_id = :user_id ORDER BY e.created_at DESC"), {"user_id": current_user["id"]}).mappings().all()
    return [dict(row) for row in result]

# ─── Get Single Expense ───────────────────────────────────────
@router.get("/{expense_id}")
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = """
        SELECT e.*, c.name as category, u.name as employee_name
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.id
        LEFT JOIN users u ON e.user_id = u.id
        WHERE e.id = :id
    """
    expense = db.execute(text(query), {"id": expense_id}).mappings().first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    if current_user.get("role") == "employee" and expense["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return dict(expense)

# ─── Update Expense ───────────────────────────────────────────
class ExpenseUpdate(BaseModel):
    title: str = None
    amount: float = None
    category_id: int = None
    description: str = None

@router.put("/{expense_id}")
def update_expense(
    expense_id: int,
    payload: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    expense = db.execute(text("SELECT * FROM expenses WHERE id = :id"), {"id": expense_id}).mappings().first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    if expense["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    if expense["status"] != "pending":
        raise HTTPException(status_code=400, detail="Only pending expenses can be edited")
        
    title = payload.title if payload.title is not None else expense["title"]
    amount = payload.amount if payload.amount is not None else expense["amount"]
    category_id = payload.category_id if payload.category_id is not None else expense["category_id"]
    description = payload.description if payload.description is not None else expense["description"]
    
    db.execute(
        text("UPDATE expenses SET title = :title, amount = :amount, category_id = :category_id, description = :description WHERE id = :id"),
        {"title": title, "amount": amount, "category_id": category_id, "description": description, "id": expense_id}
    )
    db.commit()
    return {"message": "Expense updated successfully"}

# ─── Delete Expense ───────────────────────────────────────────
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    expense = db.execute(text("SELECT * FROM expenses WHERE id = :id"), {"id": expense_id}).mappings().first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    if expense["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    if expense["status"] != "pending":
        raise HTTPException(status_code=400, detail="Only pending expenses can be deleted")
        
    db.execute(text("DELETE FROM expenses WHERE id = :id"), {"id": expense_id})
    db.commit()
    return {"message": "Expense deleted successfully"}

# ─── Approve Expense ──────────────────────────────────────────
class ApprovalAction(BaseModel):
    comment: str = ""

@router.post("/{expense_id}/approve")
def approve_expense(
    expense_id: int,
    payload: ApprovalAction,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("manager", "admin"))
):
    expense = db.execute(text("SELECT * FROM expenses WHERE id = :id"), {"id": expense_id}).mappings().first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
        
    comment = payload.comment
    db.execute(
        text("UPDATE expenses SET status = 'approved', manager_comment = :comment WHERE id = :id"),
        {"comment": comment, "id": expense_id}
    )
    db.commit()
    return {"message": "Expense approved"}

# ─── Reject Expense ───────────────────────────────────────────
@router.post("/{expense_id}/reject")
def reject_expense(
    expense_id: int,
    payload: ApprovalAction,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("manager", "admin"))
):
    expense = db.execute(text("SELECT * FROM expenses WHERE id = :id"), {"id": expense_id}).mappings().first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
        
    comment = payload.comment
    db.execute(
        text("UPDATE expenses SET status = 'rejected', manager_comment = :comment WHERE id = :id"),
        {"comment": comment, "id": expense_id}
    )
    db.commit()
    return {"message": "Expense rejected"}
