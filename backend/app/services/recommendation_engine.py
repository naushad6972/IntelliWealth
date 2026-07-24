from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import User, Transaction

def generate_savings_recommendations(db: Session, user: User) -> Dict[str, Any]:
    recommendations = []
    total_potential = 0.0

    # 1. Shopping Analysis
    shopping_amt = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user.id,
        Transaction.type == "Expense",
        Transaction.category == "Shopping"
    ).scalar() or 0.0

    if shopping_amt > (user.monthly_income * 0.15):
        potential = round(shopping_amt * 0.30, 2)
        total_potential += potential
        recommendations.append({
            "category": "Shopping",
            "title": "Reduce Impulse Online Shopping",
            "description": f"You spent ₹{shopping_amt:,.2f} on shopping. Implementing a 48-hour cool-off rule before non-essential purchases can save up to 30%.",
            "potential_savings": potential
        })

    # 2. Food & Dining Delivery
    food_amt = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user.id,
        Transaction.type == "Expense",
        Transaction.category == "Food"
    ).scalar() or 0.0

    if food_amt > (user.monthly_income * 0.12):
        potential = round(food_amt * 0.25, 2)
        total_potential += potential
        recommendations.append({
            "category": "Food",
            "title": "Optimize Food Delivery & Dining Out",
            "description": f"Food expenses stand at ₹{food_amt:,.2f}. Cooking at home during weekdays can yield significant monthly savings.",
            "potential_savings": potential
        })

    # 3. Subscriptions & Entertainment
    ent_amt = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user.id,
        Transaction.type == "Expense",
        Transaction.category == "Entertainment"
    ).scalar() or 0.0

    if ent_amt > 1500:
        potential = round(ent_amt * 0.40, 2)
        total_potential += potential
        recommendations.append({
            "category": "Entertainment",
            "title": "Audit Recurring Subscriptions",
            "description": f"Entertainment and OTT subscriptions total ₹{ent_amt:,.2f}. Consider pausing unused streaming services.",
            "potential_savings": potential
        })

    # 4. Travel & Cabs
    travel_amt = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user.id,
        Transaction.type == "Expense",
        Transaction.category == "Travel"
    ).scalar() or 0.0

    if travel_amt > (user.monthly_income * 0.10):
        potential = round(travel_amt * 0.20, 2)
        total_potential += potential
        recommendations.append({
            "category": "Travel",
            "title": "Optimize Commute & Cab Rides",
            "description": f"Cab rides and transit expenses total ₹{travel_amt:,.2f}. Switching to public transit for twice-weekly commutes saves money.",
            "potential_savings": potential
        })

    if not recommendations:
        total_potential = round(user.monthly_income * 0.10, 2)
        recommendations.append({
            "category": "General",
            "title": "Automate Pay-Yourself-First Savings",
            "description": "Transfer 10% of monthly salary into an automated high-return SIP on payday before spending.",
            "potential_savings": total_potential
        })

    return {
        "total_potential_savings": round(total_potential, 2),
        "recommendations": recommendations
    }
