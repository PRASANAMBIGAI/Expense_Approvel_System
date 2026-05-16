from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse, ApprovalAction
from utils.auth import get_current_user, require_role

router = APIRouter(prefix="/expenses", tags=["Expenses"])

# ─── Submit Expense ───────────────────────────────────────────
@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def submit_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # TODO: implement expense submission logic
    pass

# ─── Get All Expenses ─────────────────────────────────────────
@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # TODO: implement list logic (filter by role, status, category)
    pass

# ─── Get Single Expense ───────────────────────────────────────
@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # TODO: fetch single expense by ID
    pass

# ─── Update Expense ───────────────────────────────────────────
@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    payload: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # TODO: employee edits their own pending expense only
    pass

# ─── Delete Expense ───────────────────────────────────────────
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # TODO: employee deletes their own pending expense only
    pass

# ─── Approve Expense ──────────────────────────────────────────
@router.post("/{expense_id}/approve", response_model=ExpenseResponse)
def approve_expense(
    expense_id: int,
    payload: ApprovalAction,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("manager", "admin"))
):
    # TODO: manager/admin approves expense, log to ApprovalLog
    pass

# ─── Reject Expense ───────────────────────────────────────────
@router.post("/{expense_id}/reject", response_model=ExpenseResponse)
def reject_expense(
    expense_id: int,
    payload: ApprovalAction,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("manager", "admin"))
):
    # TODO: manager/admin rejects expense with comment, log to ApprovalLog
    pass
