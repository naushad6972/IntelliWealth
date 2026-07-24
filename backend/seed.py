import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import engine, SessionLocal, Base
from app.models.models import User, BankAccount, BankConsent, Transaction, Budget, Goal, Notification, SyncLog
from app.core.security import get_password_hash

def seed_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        print("Seeding IntelliWealth database...")

        # 1. Create Demo User
        demo_user = User(
            name="Alex Mercer",
            email="demo@intelliwealth.com",
            hashed_password=get_password_hash("Password123!"),
            monthly_income=125000.00,
            occupation="Senior Software Engineer",
            risk_preference="Moderate",
            financial_goals="Build Emergency Fund (₹5,00,000), Buy Electric Car, Save for Retirement",
            preferred_currency="INR"
        )
        db.add(demo_user)
        db.flush()

        # 2. Create Bank Accounts & Consents
        bank1 = BankAccount(
            user_id=demo_user.id,
            provider_id="account_aggregator",
            bank_name="HDFC Wealth Savings",
            account_number_masked="**** 8842",
            account_type="Savings",
            currency="INR",
            balance=245800.00,
            status="ACTIVE",
            auto_sync=True,
            last_synced_at=datetime.utcnow()
        )
        bank2 = BankAccount(
            user_id=demo_user.id,
            provider_id="open_banking",
            bank_name="ICICI Direct Salary",
            account_number_masked="**** 3109",
            account_type="Salary",
            currency="INR",
            balance=98400.50,
            status="ACTIVE",
            auto_sync=True,
            last_synced_at=datetime.utcnow()
        )
        db.add_all([bank1, bank2])
        db.flush()

        consent1 = BankConsent(
            user_id=demo_user.id,
            bank_account_id=bank1.id,
            provider_type="account_aggregator",
            consent_id="aa_consent_demo_8842",
            access_token="aa_token_access_demo_token_8842",
            refresh_token="aa_token_refresh_demo_token_8842",
            token_expires_at=datetime.utcnow() + timedelta(days=180),
            status="GRANTED"
        )
        consent2 = BankConsent(
            user_id=demo_user.id,
            bank_account_id=bank2.id,
            provider_type="open_banking",
            consent_id="ob_consent_demo_3109",
            access_token="ob_token_access_demo_token_3109",
            refresh_token="ob_token_refresh_demo_token_3109",
            token_expires_at=datetime.utcnow() + timedelta(days=90),
            status="GRANTED"
        )
        db.add_all([consent1, consent2])

        # 3. Create Budgets
        budgets = [
            Budget(user_id=demo_user.id, category="Food", period="Monthly", amount=15000.0, alert_threshold=0.8),
            Budget(user_id=demo_user.id, category="Shopping", period="Monthly", amount=20000.0, alert_threshold=0.8),
            Budget(user_id=demo_user.id, category="Travel", period="Monthly", amount=10000.0, alert_threshold=0.75),
            Budget(user_id=demo_user.id, category="Bills", period="Monthly", amount=12000.0, alert_threshold=0.85),
            Budget(user_id=demo_user.id, category="Entertainment", period="Monthly", amount=5000.0, alert_threshold=0.80),
            Budget(user_id=demo_user.id, category="Total Monthly Budget", period="Monthly", amount=85000.0, alert_threshold=0.80),
        ]
        db.add_all(budgets)

        # 4. Create Goals
        goals = [
            Goal(user_id=demo_user.id, title="6-Month Emergency Fund", category="Emergency Fund", target_amount=400000.0, current_amount=245000.0, deadline="2026-12-31", status="IN_PROGRESS"),
            Goal(user_id=demo_user.id, title="Electric EV Car Downpayment", category="Car", target_amount=300000.0, current_amount=120000.0, deadline="2027-06-30", status="IN_PROGRESS"),
            Goal(user_id=demo_user.id, title="Japan Vacation 2027", category="Vacation", target_amount=200000.0, current_amount=65000.0, deadline="2027-04-15", status="IN_PROGRESS"),
            Goal(user_id=demo_user.id, title="Retirement Corpus Compounder", category="Retirement", target_amount=10000000.0, current_amount=850000.0, deadline="2040-01-01", status="IN_PROGRESS"),
        ]
        db.add_all(goals)

        # 5. Generate 100+ Realistic Transactions over recent months
        merchants_pool = [
            ("Salary Credit TechCorp", 125000.0, "Income", "Salary", "Bank Transfer"),
            ("Freelance Consulting", 25000.0, "Income", "Salary", "UPI"),
            ("Swiggy Gourmet", 680.0, "Expense", "Food", "UPI"),
            ("Zomato Delivery", 540.0, "Expense", "Food", "UPI"),
            ("Starbucks Reserve", 420.0, "Expense", "Food", "Debit Card"),
            ("DMart Supermarket", 4800.0, "Expense", "Food", "Credit Card"),
            ("Blinkit Quick Grocery", 850.0, "Expense", "Food", "UPI"),
            ("Amazon Electronics", 14999.0, "Expense", "Shopping", "Credit Card"),
            ("Myntra Fashion", 3499.0, "Expense", "Shopping", "Credit Card"),
            ("Zara Apparel", 5990.0, "Expense", "Shopping", "Credit Card"),
            ("Uber Transit", 450.0, "Expense", "Travel", "UPI"),
            ("Ola Auto", 180.0, "Expense", "Travel", "UPI"),
            ("IRCTC Railway Ticket", 1850.0, "Expense", "Travel", "UPI"),
            ("HPCL Fuel Station", 3200.0, "Expense", "Fuel", "Credit Card"),
            ("Airtel Broadband", 1179.0, "Expense", "Bills", "UPI"),
            ("BESCOM Electricity Bill", 2450.0, "Expense", "Bills", "Bank Transfer"),
            ("Netflix 4K Plan", 649.0, "Expense", "Entertainment", "Credit Card"),
            ("BookMyShow Cinema", 890.0, "Expense", "Entertainment", "UPI"),
            ("Zerodha Nifty 50 Index SIP", 25000.0, "Expense", "Investment", "Bank Transfer"),
            ("Groww Flexi Cap SIP", 15000.0, "Expense", "Investment", "Bank Transfer"),
            ("Apollo Pharmacy", 950.0, "Expense", "Healthcare", "UPI"),
            ("Udemy Python ML Course", 499.0, "Expense", "Education", "UPI"),
            ("HDFC ERGO Health Insurance", 18500.0, "Expense", "Insurance", "Bank Transfer")
        ]

        today = datetime.now()
        transactions = []
        
        # 4 months of transactions
        for m in range(4):
            # Monthly salary on 1st
            sal_date = (today - timedelta(days=m * 30)).replace(day=1).strftime("%Y-%m-%d")
            transactions.append(Transaction(
                user_id=demo_user.id,
                bank_account_id=bank2.id,
                date=sal_date,
                merchant="Salary Credit TechCorp",
                amount=125000.0,
                type="Income",
                category="Salary",
                payment_method="Bank Transfer",
                notes="Monthly Salary Credit",
                categorizer_type="RULE"
            ))

            # Regular expenses
            for i in range(25):
                days_offset = (m * 30) + random.randint(1, 28)
                tx_date = (today - timedelta(days=days_offset)).strftime("%Y-%m-%d")
                merch, base_amt, tx_type, cat, pay_method = random.choice(merchants_pool[2:])
                amt = round(base_amt * random.uniform(0.85, 1.25), 2)

                transactions.append(Transaction(
                    user_id=demo_user.id,
                    bank_account_id=random.choice([bank1.id, bank2.id]),
                    date=tx_date,
                    merchant=merch,
                    amount=amt,
                    type=tx_type,
                    category=cat,
                    payment_method=pay_method,
                    confidence_score=0.95,
                    categorizer_type="ML"
                ))

        db.add_all(transactions)

        # 6. Add Initial Notifications
        notifications = [
            Notification(user_id=demo_user.id, type="BUDGET_WARNING", title="Shopping Budget Alert", message="You have used 85% of your monthly Shopping budget.", is_read=False),
            Notification(user_id=demo_user.id, type="GOAL_REMINDER", title="Emergency Fund Goal", message="You are on track to complete your 6-Month Emergency Fund by Dec 2026!", is_read=False),
            Notification(user_id=demo_user.id, type="SUBSCRIPTION", title="Netflix Renewal Reminder", message="Upcoming recurring charge of ₹649 for Netflix 4K Plan.", is_read=True)
        ]
        db.add_all(notifications)

        db.commit()
        print("✅ Database successfully seeded with 100+ transactions and demo user (demo@intelliwealth.com / Password123!)")

    except Exception as e:
        print(f"❌ Seeding error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
