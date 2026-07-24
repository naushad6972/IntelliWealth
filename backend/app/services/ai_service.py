import logging
import json
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.config import settings
from app.models.models import User, Transaction, Budget, Goal, BankAccount

logger = logging.getLogger(__name__)

# Try loading Google Gemini or OpenAI if keys exist
gemini_client = None
if settings.GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        gemini_client = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        logger.warning(f"Failed to initialize Gemini API: {e}")

class AIService:
    @staticmethod
    def process_chat_message(db: Session, user: User, user_message: str) -> Dict[str, Any]:
        """
        Processes financial natural language query using user's real financial context
        (Income, Expenses, Budgets, Health Score, Transactions).
        """
        msg_lower = user_message.lower()

        # Build Financial Context Summary
        total_income = user.monthly_income or 50000.0
        total_expense = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user.id,
            Transaction.type == "Expense"
        ).scalar() or 0.0

        savings = max(0.0, total_income - total_expense)

        food_exp = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user.id,
            Transaction.type == "Expense",
            Transaction.category == "Food"
        ).scalar() or 0.0

        shopping_exp = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user.id,
            Transaction.type == "Expense",
            Transaction.category == "Shopping"
        ).scalar() or 0.0

        # Attempt Gemini API if available
        if gemini_client:
            try:
                system_prompt = f"""
                You are IntelliWealth, an expert AI Financial Coach.
                User Context:
                - Name: {user.name}
                - Monthly Income: ₹{user.monthly_income:,.2f}
                - Total Monthly Expense: ₹{total_expense:,.2f}
                - Current Monthly Savings: ₹{savings:,.2f}
                - Food Expense: ₹{food_exp:,.2f}
                - Shopping Expense: ₹{shopping_exp:,.2f}
                - Risk Preference: {user.risk_preference}

                User Question: "{user_message}"
                Answer concisely in bullet points or markdown paragraphs. Give accurate, actionable financial guidance based on their real financial context.
                """
                response = gemini_client.generate_content(system_prompt)
                if response and response.text:
                    return {
                        "response": response.text,
                        "suggested_actions": ["View Expense Analytics", "Check Budget Limits", "Generate Savings Plan"]
                    }
            except Exception as e:
                logger.warning(f"Gemini API error, falling back to rule-based NLP: {e}")

        # High-Quality Rule-Based Natural Language Fallback Engine
        if any(k in msg_lower for k in ["food", "dining", "swiggy", "zomato"]):
            reply = f"You have spent **₹{food_exp:,.2f}** on Food & Dining. This represents **{((food_exp/total_income)*100 if total_income>0 else 0):.1f}%** of your monthly income. " \
                    f"Consider setting a Food Budget cap to keep dining out within 10% of monthly earnings."
            suggested = ["Set Food Budget", "View Category Analytics", "Check Savings Tips"]

        elif any(k in msg_lower for k in ["shopping", "amazon", "flipkart"]):
            reply = f"Your total Shopping expenditure is **₹{shopping_exp:,.2f}**. " \
                    f"To save money on shopping, try delaying non-essential purchases by 48 hours to curb impulse buying."
            suggested = ["Set Shopping Budget", "View Top Merchants"]

        elif any(k in msg_lower for k in ["save", "saving", "5000", "reduce expense"]):
            reply = f"Based on your cash flow (Income: ₹{total_income:,.2f}, Expenses: ₹{total_expense:,.2f}), here is how you can save an extra **₹5,000/month**:\n\n" \
                    f"1. **Food & Dining**: Cut 2 weekend delivery orders (Save ~₹1,500).\n" \
                    f"2. **Shopping**: Pause non-essential clothing/electronics (Save ~₹2,000).\n" \
                    f"3. **Subscriptions**: Cancel 2 unused OTT or app memberships (Save ~₹800).\n" \
                    f"4. **Cabs & Transit**: Switch 2 weekly cab rides to metro (Save ~₹700)."
            suggested = ["Create Goal", "View Recommendation Engine"]

        elif any(k in msg_lower for k in ["score", "health", "why low"]):
            reply = f"Your Financial Health Score is calculated across 5 core indicators: Savings Rate, Emergency Fund, Budget Discipline, Investment Ratio, and Discretionary Ratio.\n\n" \
                    f"To boost your score:\n" \
                    f"• Maintain a liquid emergency fund covering 6 months of expenses.\n" \
                    f"• Automate 15% of income into monthly equity index SIPs.\n" \
                    f"• Stay strictly within your category budget limits."
            suggested = ["Open Health Score Page", "Set Category Budgets"]

        elif any(k in msg_lower for k in ["sip", "mutual fund", "etf", "invest"]):
            reply = f"**SIP (Systematic Investment Plan)** lets you invest fixed monthly amounts into mutual funds, gaining from Rupee Cost Averaging and Compounding.\n\n" \
                    f"• **For Beginners**: Nifty 50 Index Fund via Direct Plan Growth.\n" \
                    f"• **Educational Suggestion**: Based on your ₹{user.monthly_income:,.2f} income, consider learning with a test SIP of ₹3,000 - ₹5,000/month after establishing an emergency fund."
            suggested = ["Explore Investment Modules", "Calculate Goal Savings"]

        else:
            reply = f"Hello {user.name}! I am your IntelliWealth AI Financial Assistant. Here is your quick financial summary:\n\n" \
                    f"• **Monthly Income**: ₹{user.monthly_income:,.2f}\n" \
                    f"• **Total Expenses**: ₹{total_expense:,.2f}\n" \
                    f"• **Net Savings**: ₹{savings:,.2f}\n\n" \
                    f"You can ask me questions like: *'How much did I spend on food?'*, *'How can I save ₹5,000?'*, *'Explain SIP'*, or *'Why is my health score low?'*"
            suggested = ["How much did I spend on food?", "How can I save ₹5,000?", "Explain SIP"]

        return {
            "response": reply,
            "suggested_actions": suggested
        }

    @staticmethod
    def generate_educational_investment_suggestions(db: Session, user: User, topic_id: str) -> Dict[str, Any]:
        """
        Generates personalized educational investment suggestions based on user context.
        Includes mandatory compliance disclaimer.
        """
        total_income = user.monthly_income or 50000.0
        total_expense = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user.id,
            Transaction.type == "Expense"
        ).scalar() or 0.0

        savings = max(0.0, total_income - total_expense)
        suggested_learning_sip = round(savings * 0.30, 2) if savings > 0 else round(total_income * 0.10, 2)

        suggestions = [
            f"You currently save ₹{savings:,.2f} per month from your monthly income of ₹{total_income:,.2f}.",
            "Step 1: Ensure you have built a 6-month liquid emergency fund in a high-yield savings account or liquid mutual fund.",
            f"Step 2: For educational learning purposes, consider exploring low-cost Nifty 50 Direct Index Funds with an initial monthly SIP of ₹{suggested_learning_sip:,.2f}.",
            f"Step 3: Align your investments with your risk preference ({user.risk_preference}) and target goals."
        ]

        disclaimer = "DISCLAIMER: IntelliWealth provides financial education and automated analytical insights for informational and learning purposes only. This does not constitute personalized financial or investment advice. Consult a SEBI registered investment advisor before making financial decisions."

        return {
            "topic_id": topic_id,
            "user_context_summary": f"Income: ₹{total_income:,.2f} | Savings: ₹{savings:,.2f} | Risk: {user.risk_preference}",
            "educational_suggestions": suggestions,
            "suggested_learning_investment": suggested_learning_sip,
            "disclaimer": disclaimer
        }

