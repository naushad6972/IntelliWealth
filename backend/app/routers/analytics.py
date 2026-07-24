from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.models import User, Transaction, BankAccount
from app.schemas.schemas import DashboardOverview, ExpenseAnalyticsOut, TransactionOut
from app.core.deps import get_current_user
from app.utils.cache import cache
import json

router = APIRouter(prefix="/analytics", tags=["Analytics & Dashboard"])

@router.get("/dashboard", response_model=DashboardOverview)
def get_dashboard_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cache_key = f"dashboard:{current_user.id}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    # Total Income & Expenses calculation
    total_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "Income"
    ).scalar() or 0.0

    total_expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "Expense"
    ).scalar() or 0.0

    savings = total_income - total_expense
    savings_rate = round((savings / total_income * 100), 1) if total_income > 0 else 0.0

    # Bank Accounts balance sum
    bank_balances = db.query(func.sum(BankAccount.balance)).filter(
        BankAccount.user_id == current_user.id,
        BankAccount.status == "ACTIVE"
    ).scalar() or 0.0

    current_balance = bank_balances if bank_balances > 0 else (current_user.monthly_income + savings)

    # Recent 5 transactions
    recent_txs = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).order_by(Transaction.date.desc(), Transaction.id.desc()).limit(6).all()

    # Category distribution for Expenses
    cat_query = db.query(
        Transaction.category, func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "Expense"
    ).group_by(Transaction.category).all()

    category_distribution = [
        {"category": cat, "amount": round(amt, 2)}
        for cat, amt in cat_query
    ]

    # Monthly Cash Flow (Last 6 Months)
    # Generate month buckets
    monthly_cash_flow = []
    today = datetime.now()
    for i in range(5, -1, -1):
        m_date = today - timedelta(days=i * 30)
        m_str = m_date.strftime("%b %Y")
        m_prefix = m_date.strftime("%Y-%m")

        inc = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.type == "Income",
            Transaction.date.like(f"{m_prefix}%")
        ).scalar() or 0.0

        exp = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.type == "Expense",
            Transaction.date.like(f"{m_prefix}%")
        ).scalar() or 0.0

        monthly_cash_flow.append({
            "month": m_str,
            "income": round(inc, 2),
            "expense": round(exp, 2),
            "savings": round(inc - exp, 2)
        })

    result = DashboardOverview(
        total_income=round(total_income, 2),
        total_expense=round(total_expense, 2),
        savings=round(savings, 2),
        current_balance=round(current_balance, 2),
        savings_rate=savings_rate,
        recent_transactions=[TransactionOut.model_validate(t) for t in recent_txs],
        monthly_cash_flow=monthly_cash_flow,
        category_distribution=category_distribution
    )
    # Cache dashboard for 20 seconds to reduce repeated DB load during navigation
    cache.set(cache_key, result, ttl_seconds=20)
    return result

@router.get("/expense", response_model=ExpenseAnalyticsOut)
def get_expense_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cache_key = f"expense_analytics:{current_user.id}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    # Category-wise expense breakdown
    cat_query = db.query(
        Transaction.category, func.sum(Transaction.amount), func.count(Transaction.id)
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "Expense"
    ).group_by(Transaction.category).all()

    total_expense = sum(amt for _, amt, _ in cat_query) or 1.0

    category_wise = [
        {
            "category": cat,
            "amount": round(amt, 2),
            "count": count,
            "percentage": round((amt / total_expense) * 100, 1)
        }
        for cat, amt, count in cat_query
    ]

    # Top Merchants
    top_merchants_query = db.query(
        Transaction.merchant, func.sum(Transaction.amount), func.count(Transaction.id)
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "Expense"
    ).group_by(Transaction.merchant).order_by(func.sum(Transaction.amount).desc()).limit(6).all()

    top_merchants = [
        {"merchant": m, "amount": round(amt, 2), "transactions_count": count}
        for m, amt, count in top_merchants_query
    ]

    # Recurring Expenses
    recurring_query = db.query(
        Transaction.merchant, Transaction.category, Transaction.amount
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "Expense",
        Transaction.category.in_(["Bills", "Rent", "Entertainment", "Insurance"])
    ).group_by(Transaction.merchant).limit(5).all()

    recurring_expenses = [
        {"merchant": m, "category": cat, "monthly_amount": round(amt, 2)}
        for m, cat, amt in recurring_query
    ]

    # Weekend Spending calculation
    # Fetch only needed fields for weekend/heatmap calculations to reduce ORM overhead
    txs = db.query(Transaction.date, Transaction.amount).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "Expense"
    ).all()

    weekend_total = 0.0
    weekday_total = 0.0
    for date_val, amt in txs:
        try:
            dt = datetime.strptime(date_val, "%Y-%m-%d")
            if dt.weekday() >= 5:  # Saturday & Sunday
                weekend_total += amt
            else:
                weekday_total += amt
        except ValueError:
            pass

    weekend_spending = {
        "weekend_total": round(weekend_total, 2),
        "weekday_total": round(weekday_total, 2),
        "weekend_percentage": round((weekend_total / (weekend_total + weekday_total) * 100), 1) if (weekend_total + weekday_total) > 0 else 0.0
    }

    # Heatmap (Day of week vs Spending intensity)
    days_spending = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0}
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for date_val, amt in txs:
        try:
            dt = datetime.strptime(date_val, "%Y-%m-%d")
            days_spending[dt.weekday()] += amt
        except ValueError:
            pass

    heatmap = [
        {"day": day_names[day_idx], "amount": round(amt, 2)}
        for day_idx, amt in days_spending.items()
    ]

    # Income vs Expense trend over recent months
    trend = []
    today = datetime.now()
    for i in range(5, -1, -1):
        m_date = today - timedelta(days=i * 30)
        m_str = m_date.strftime("%b %Y")
        m_prefix = m_date.strftime("%Y-%m")

        inc = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.type == "Income",
            Transaction.date.like(f"{m_prefix}%")
        ).scalar() or 0.0

        exp = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.type == "Expense",
            Transaction.date.like(f"{m_prefix}%")
        ).scalar() or 0.0

        trend.append({
            "month": m_str,
            "income": round(inc, 2),
            "expense": round(exp, 2)
        })

    result = ExpenseAnalyticsOut(
        category_wise=category_wise,
        top_merchants=top_merchants,
        recurring_expenses=recurring_expenses,
        weekend_spending=weekend_spending,
        heatmap=heatmap,
        income_vs_expense_trend=trend
    )
    cache.set(cache_key, result, ttl_seconds=30)
    return result
