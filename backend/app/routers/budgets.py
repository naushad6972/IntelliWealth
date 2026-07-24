from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime

from app.db.session import get_db
from app.models.models import User, Budget, Transaction, Notification
from app.schemas.schemas import BudgetCreate, BudgetOut
from app.core.deps import get_current_user

router = APIRouter(prefix="/budgets", tags=["Budget Planner"])

@router.get("", response_model=List[BudgetOut])
def get_budgets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    budgets = db.query(Budget).filter(Budget.user_id == current_user.id).all()
    current_month_prefix = datetime.now().strftime("%Y-%m")

    result = []
    for b in budgets:
        # Calculate spent amount for category in current month
        if b.category == "Total Monthly Budget":
            spent = db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == current_user.id,
                Transaction.type == "Expense",
                Transaction.date.like(f"{current_month_prefix}%")
            ).scalar() or 0.0
        else:
            spent = db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == current_user.id,
                Transaction.type == "Expense",
                Transaction.category == b.category,
                Transaction.date.like(f"{current_month_prefix}%")
            ).scalar() or 0.0

        remaining = max(0.0, b.amount - spent)
        pct = round((spent / b.amount) * 100, 1) if b.amount > 0 else 0.0

        status_str = "OK"
        if pct >= 100:
            status_str = "OVERSPENT"
        elif pct >= (b.alert_threshold * 100):
            status_str = "WARNING"

        result.append(BudgetOut(
            id=b.id,
            category=b.category,
            period=b.period,
            amount=b.amount,
            spent_amount=round(spent, 2),
            remaining_amount=round(remaining, 2),
            percentage_used=pct,
            status=status_str,
            alert_threshold=b.alert_threshold,
            created_at=b.created_at
        ))

    return result

@router.post("", response_model=BudgetOut, status_code=status.HTTP_201_CREATED)
def create_budget(
    b_in: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Budget).filter(
        Budget.user_id == current_user.id,
        Budget.category == b_in.category
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Budget for category '{b_in.category}' already exists. Update it instead."
        )

    budget = Budget(
        user_id=current_user.id,
        category=b_in.category,
        period=b_in.period,
        amount=b_in.amount,
        alert_threshold=b_in.alert_threshold
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)

    return BudgetOut(
        id=budget.id,
        category=budget.category,
        period=budget.period,
        amount=budget.amount,
        spent_amount=0.0,
        remaining_amount=budget.amount,
        percentage_used=0.0,
        status="OK",
        alert_threshold=budget.alert_threshold,
        created_at=budget.created_at
    )

@router.put("/{budget_id}", response_model=BudgetOut)
def update_budget(
    budget_id: int,
    b_in: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    budget = db.query(Budget).filter(Budget.id == budget_id, Budget.user_id == current_user.id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found.")

    budget.category = b_in.category
    budget.period = b_in.period
    budget.amount = b_in.amount
    budget.alert_threshold = b_in.alert_threshold
    db.commit()
    db.refresh(budget)

    # Return refreshed budget status
    current_month_prefix = datetime.now().strftime("%Y-%m")
    spent = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "Expense",
        Transaction.category == budget.category,
        Transaction.date.like(f"{current_month_prefix}%")
    ).scalar() or 0.0

    remaining = max(0.0, budget.amount - spent)
    pct = round((spent / budget.amount) * 100, 1) if budget.amount > 0 else 0.0

    return BudgetOut(
        id=budget.id,
        category=budget.category,
        period=budget.period,
        amount=budget.amount,
        spent_amount=round(spent, 2),
        remaining_amount=round(remaining, 2),
        percentage_used=pct,
        status="OVERSPENT" if pct >= 100 else ("WARNING" if pct >= budget.alert_threshold * 100 else "OK"),
        alert_threshold=budget.alert_threshold,
        created_at=budget.created_at
    )

@router.delete("/{budget_id}")
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    budget = db.query(Budget).filter(Budget.id == budget_id, Budget.user_id == current_user.id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found.")
    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted successfully."}
