from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.session import get_db
from app.models.models import User, Notification, Budget, Transaction, Goal
from app.schemas.schemas import NotificationOut
from app.core.deps import get_current_user
from sqlalchemy import func

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=List[NotificationOut])
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).all()

    if not notifications:
        # Generate dynamic notifications check
        generate_notifications_for_user(db, current_user)
        notifications = db.query(Notification).filter(
            Notification.user_id == current_user.id
        ).order_by(Notification.created_at.desc()).all()

    return notifications

@router.post("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    n = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    if not n:
        raise HTTPException(status_code=404, detail="Notification not found.")

    n.is_read = True
    db.commit()
    return {"message": "Notification marked as read."}

@router.post("/generate-alerts")
def trigger_alert_evaluation(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    generate_notifications_for_user(db, current_user)
    return {"message": "Alert evaluation triggered."}

def generate_notifications_for_user(db: Session, user: User):
    # 1. Budget Overspending Check
    budgets = db.query(Budget).filter(Budget.user_id == user.id).all()
    m_prefix = datetime.now().strftime("%Y-%m")

    for b in budgets:
        spent = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user.id,
            Transaction.category == b.category,
            Transaction.type == "Expense",
            Transaction.date.like(f"{m_prefix}%")
        ).scalar() or 0.0

        if spent >= b.amount:
            _add_notif_if_new(db, user.id, "BUDGET_WARNING", f"Budget Overspent: {b.category}", f"You have exceeded your monthly {b.category} budget limit of ₹{b.amount:,.2f} (Spent: ₹{spent:,.2f}).")
        elif spent >= (b.amount * b.alert_threshold):
            _add_notif_if_new(db, user.id, "BUDGET_WARNING", f"Budget Alert: {b.category}", f"You have used over {int(b.alert_threshold*100)}% of your {b.category} budget (Spent: ₹{spent:,.2f} / ₹{b.amount:,.2f}).")

    # 2. Goal Progress Reminder
    goals = db.query(Goal).filter(Goal.user_id == user.id, Goal.status == "IN_PROGRESS").all()
    for g in goals:
        pct = (g.current_amount / g.target_amount * 100) if g.target_amount > 0 else 0
        if pct < 50:
            _add_notif_if_new(db, user.id, "GOAL_REMINDER", f"Goal Milestone Reminder: {g.title}", f"You are at {pct:.1f}% for '{g.title}'. Deposit ₹{g.target_amount - g.current_amount:,.2f} to hit your deadline.")

    # 3. Monthly Summary Alert
    _add_notif_if_new(db, user.id, "MONTHLY_SUMMARY", "Monthly Financial Report Available", "Your monthly financial audit report and spending breakdown is ready for download in Reports.")

def _add_notif_if_new(db: Session, user_id: int, notif_type: str, title: str, message: str):
    existing = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.type == notif_type,
        Notification.title == title
    ).first()

    if not existing:
        notif = Notification(
            user_id=user_id,
            type=notif_type,
            title=title,
            message=message,
            is_read=False
        )
        db.add(notif)
        db.commit()
