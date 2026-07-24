from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import User, Transaction, Budget, Goal, BankAccount

def calculate_financial_health_score(db: Session, user: User) -> Dict[str, Any]:
    income = user.monthly_income or 50000.0

    # Total expenses
    total_expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user.id,
        Transaction.type == "Expense"
    ).scalar() or 0.0

    # Savings & Savings Rate
    monthly_savings = max(0.0, income - total_expense)
    savings_rate = (monthly_savings / income * 100) if income > 0 else 0.0

    # 1. Savings Rate Score (Max 25 pts)
    # Goal: >= 30% savings rate for max points
    savings_score = min(25.0, (savings_rate / 30.0) * 25.0)

    # 2. Budget Discipline (Max 20 pts)
    budgets = db.query(Budget).filter(Budget.user_id == user.id).all()
    if budgets:
        overspent_count = 0
        for b in budgets:
            spent = db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user.id,
                Transaction.category == b.category,
                Transaction.type == "Expense"
            ).scalar() or 0.0
            if spent > b.amount:
                overspent_count += 1
        budget_score = max(0.0, 20.0 - (overspent_count * 5.0))
    else:
        budget_score = 12.0  # neutral score if no budgets created yet

    # 3. Emergency Fund Readiness (Max 20 pts)
    # Check liquidity balance vs 6 months expenses
    liquid_balance = db.query(func.sum(BankAccount.balance)).filter(
        BankAccount.user_id == user.id,
        BankAccount.status == "ACTIVE"
    ).scalar() or monthly_savings * 3

    six_month_target = (total_expense or income * 0.7) * 6
    emergency_ratio = (liquid_balance / six_month_target) if six_month_target > 0 else 0.5
    emergency_score = min(20.0, emergency_ratio * 20.0)

    # 4. Investment Habit (Max 20 pts)
    invested_amt = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user.id,
        Transaction.category == "Investment"
    ).scalar() or 0.0

    investment_ratio = (invested_amt / income) if income > 0 else 0.0
    investment_score = min(20.0, (investment_ratio / 0.15) * 20.0)  # 15% target investment

    # 5. Debt / Discretionary Ratio (Max 15 pts)
    shopping_food_amt = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user.id,
        Transaction.category.in_(["Shopping", "Food", "Entertainment"])
    ).scalar() or 0.0

    discretionary_ratio = (shopping_food_amt / income) if income > 0 else 0.3
    debt_discretionary_score = max(0.0, 15.0 - max(0.0, (discretionary_ratio - 0.25) * 40.0))

    final_score = int(round(savings_score + budget_score + emergency_score + investment_score + debt_discretionary_score))
    final_score = max(0, min(100, final_score))

    if final_score >= 80:
        rating = "Excellent"
    elif final_score >= 65:
        rating = "Good"
    elif final_score >= 50:
        rating = "Average"
    else:
        rating = "Poor"

    improvements = []
    if savings_rate < 20:
        improvements.append(f"Increase your savings rate from {savings_rate:.1f}% to at least 20% by cutting non-essential expenses.")
    if emergency_score < 15:
        improvements.append("Build a 6-month liquid emergency fund in a high-yield savings account or liquid mutual fund.")
    if investment_score < 12:
        improvements.append("Automate a monthly SIP in diversified equity/index mutual funds representing 15% of monthly income.")
    if budget_score < 15:
        improvements.append("Set category budgets for Shopping and Food & Dining to prevent overspending alerts.")
    if debt_discretionary_score < 10:
        improvements.append("Discretionary spending (Food, Shopping, Entertainment) exceeds 30% of income. Limit weekend dining out.")

    if not improvements:
        improvements.append("Outstanding financial discipline! Consider stepping up equity investments to accelerate financial freedom.")

    metrics = {
        "savings_rate_pct": round(savings_rate, 1),
        "savings_score": round(savings_score, 1),
        "budget_discipline_score": round(budget_score, 1),
        "emergency_fund_score": round(emergency_score, 1),
        "investment_score": round(investment_score, 1),
        "discretionary_spending_score": round(debt_discretionary_score, 1)
    }

    return {
        "score": final_score,
        "rating": rating,
        "metrics": metrics,
        "improvements": improvements
    }
