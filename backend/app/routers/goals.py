from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.session import get_db
from app.models.models import User, Goal
from app.schemas.schemas import GoalCreate, GoalOut, GoalContribution
from app.core.deps import get_current_user

router = APIRouter(prefix="/goals", tags=["Goal Planner"])

def format_goal_out(g: Goal) -> GoalOut:
    pct = round((g.current_amount / g.target_amount * 100), 1) if g.target_amount > 0 else 0.0
    pct = min(100.0, pct)

    # Calculate AI monthly saving suggestion based on deadline
    remaining_amt = max(0.0, g.target_amount - g.current_amount)
    try:
        deadline_dt = datetime.strptime(g.deadline, "%Y-%m-%d")
        now = datetime.now()
        months_left = max(1, (deadline_dt.year - now.year) * 12 + (deadline_dt.month - now.month))
    except ValueError:
        months_left = 12

    ai_monthly = round(remaining_amt / months_left, 2) if remaining_amt > 0 else 0.0

    return GoalOut(
        id=g.id,
        title=g.title,
        category=g.category,
        target_amount=g.target_amount,
        current_amount=g.current_amount,
        deadline=g.deadline,
        progress_percentage=pct,
        expected_completion_date=g.deadline,
        ai_monthly_saving_suggestion=ai_monthly,
        status="COMPLETED" if pct >= 100 else g.status,
        created_at=g.created_at
    )

@router.get("", response_model=List[GoalOut])
def get_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goals = db.query(Goal).filter(Goal.user_id == current_user.id).all()
    return [format_goal_out(g) for g in goals]

@router.post("", response_model=GoalOut, status_code=status.HTTP_201_CREATED)
def create_goal(
    g_in: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = Goal(
        user_id=current_user.id,
        title=g_in.title,
        category=g_in.category,
        target_amount=g_in.target_amount,
        current_amount=g_in.current_amount,
        deadline=g_in.deadline,
        status="IN_PROGRESS"
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return format_goal_out(goal)

@router.post("/{goal_id}/contribute", response_model=GoalOut)
def contribute_to_goal(
    goal_id: int,
    contrib: GoalContribution,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found.")

    goal.current_amount += contrib.amount
    if goal.current_amount >= goal.target_amount:
        goal.status = "COMPLETED"

    db.commit()
    db.refresh(goal)
    return format_goal_out(goal)

@router.delete("/{goal_id}")
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found.")
    db.delete(goal)
    db.commit()
    return {"message": "Goal deleted successfully."}
