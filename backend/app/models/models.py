from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.session import Base

class RiskPreferenceEnum(str, enum.Enum):
    CONSERVATIVE = "Conservative"
    MODERATE = "Moderate"
    AGGRESSIVE = "Aggressive"

class TransactionTypeEnum(str, enum.Enum):
    EXPENSE = "Expense"
    INCOME = "Income"
    TRANSFER = "Transfer"

class TransactionCategoryEnum(str, enum.Enum):
    FOOD = "Food"
    SHOPPING = "Shopping"
    TRAVEL = "Travel"
    BILLS = "Bills"
    HEALTHCARE = "Healthcare"
    ENTERTAINMENT = "Entertainment"
    EDUCATION = "Education"
    SALARY = "Salary"
    INVESTMENT = "Investment"
    RENT = "Rent"
    FUEL = "Fuel"
    INSURANCE = "Insurance"
    MISCELLANEOUS = "Miscellaneous"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    monthly_income = Column(Float, default=0.0)
    occupation = Column(String, default="Professional")
    risk_preference = Column(String, default="Moderate")
    financial_goals = Column(Text, default="Build Emergency Fund, Save for Retirement")
    preferred_currency = Column(String, default="INR")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bank_accounts = relationship("BankAccount", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    chat_histories = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    sync_logs = relationship("SyncLog", back_populates="user", cascade="all, delete-orphan")

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Indexing user_id to speed up per-user lookups
    __table_args__ = ()
    provider_id = Column(String, nullable=False)  # open_banking, account_aggregator, plaid, mock
    bank_name = Column(String, nullable=False)
    account_number_masked = Column(String, nullable=False)
    account_type = Column(String, default="Savings")  # Savings, Checking, Credit
    currency = Column(String, default="INR")
    balance = Column(Float, default=0.0)
    status = Column(String, default="ACTIVE")  # ACTIVE, DISCONNECTED, ERROR
    auto_sync = Column(Boolean, default=True)
    last_synced_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bank_accounts")
    consent = relationship("BankConsent", back_populates="bank_account", uselist=False, cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="bank_account")
    sync_logs = relationship("SyncLog", back_populates="bank_account")

class BankConsent(Base):
    __tablename__ = "bank_consents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    provider_type = Column(String, nullable=False)  # open_banking, account_aggregator, plaid
    consent_id = Column(String, unique=True, index=True, nullable=False)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)
    status = Column(String, default="GRANTED")  # GRANTED, EXPIRED, REVOKED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bank_account = relationship("BankAccount", back_populates="consent")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=True)
    date = Column(String, nullable=False, index=True)  # YYYY-MM-DD
    date = Column(String, nullable=False)  # YYYY-MM-DD
    merchant = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, default="Expense")  # Expense, Income, Transfer
    category = Column(String, default="Miscellaneous")
    payment_method = Column(String, default="UPI/Bank")  # UPI, Credit Card, Debit Card, Bank Transfer, Cash
    notes = Column(Text, nullable=True)
    raw_description = Column(String, nullable=True)
    is_recurring = Column(Boolean, default=False)
    confidence_score = Column(Float, default=1.0)
    categorizer_type = Column(String, default="RULE")  # RULE, ML, LLM, MANUAL
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
    bank_account = relationship("BankAccount", back_populates="transactions")

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category = Column(String, nullable=False)  # Category name or "Monthly Total"
    period = Column(String, default="Monthly")  # Monthly, Weekly
    amount = Column(Float, nullable=False)
    alert_threshold = Column(Float, default=0.8)  # Alert when 80% used
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="budgets")

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    category = Column(String, default="Savings")  # Emergency Fund, Vacation, Bike, Car, House, Education, Retirement
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    deadline = Column(String, nullable=False)  # YYYY-MM-DD
    status = Column(String, default="IN_PROGRESS")  # IN_PROGRESS, COMPLETED, PAUSED
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="goals")

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    role = Column(String, nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_histories")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String, nullable=False)  # BUDGET_WARNING, GOAL_REMINDER, UNUSUAL_SPENDING, SUBSCRIPTION, LOW_SAVINGS, MONTHLY_SUMMARY
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")

class SyncLog(Base):
    __tablename__ = "sync_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=True)
    sync_type = Column(String, default="MANUAL")  # MANUAL, AUTO_BACKGROUND, CSV_UPLOAD
    status = Column(String, nullable=False)  # SUCCESS, FAILED
    transactions_added = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sync_logs")
    bank_account = relationship("BankAccount", back_populates="sync_logs")
