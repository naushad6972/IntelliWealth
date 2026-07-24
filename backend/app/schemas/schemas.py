from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Auth & User Profile ---
class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    monthly_income: Optional[float] = 50000.0
    occupation: Optional[str] = "Software Engineer"
    risk_preference: Optional[str] = "Moderate"
    financial_goals: Optional[str] = "Save for emergency fund & investment"
    preferred_currency: Optional[str] = "INR"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserProfile"

class UserProfile(BaseModel):
    id: int
    name: str
    email: str
    monthly_income: float
    occupation: str
    risk_preference: str
    financial_goals: str
    preferred_currency: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    monthly_income: Optional[float] = None
    occupation: Optional[str] = None
    risk_preference: Optional[str] = None
    financial_goals: Optional[str] = None
    preferred_currency: Optional[str] = None

# --- Bank & Integration Schemas ---
class BankAccountOut(BaseModel):
    id: int
    provider_id: str
    bank_name: str
    account_number_masked: str
    account_type: str
    currency: str
    balance: float
    status: str
    auto_sync: bool
    last_synced_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class BankConsentInitiateRequest(BaseModel):
    provider_id: str  # open_banking, account_aggregator, plaid, mock
    bank_name: str
    account_type: Optional[str] = "Savings"

class BankConsentInitiateResponse(BaseModel):
    redirect_url: str
    consent_id: str
    provider_id: str
    message: str

class BankConsentCallbackRequest(BaseModel):
    provider_id: str
    consent_id: str
    code: str

# --- Transaction Schemas ---
class TransactionCreate(BaseModel):
    date: str
    merchant: str
    amount: float
    type: str = "Expense"  # Expense, Income, Transfer
    category: Optional[str] = None  # If None, AI categorizes automatically
    payment_method: Optional[str] = "UPI/Bank"
    notes: Optional[str] = None
    bank_account_id: Optional[int] = None

class TransactionUpdate(BaseModel):
    date: Optional[str] = None
    merchant: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None

class TransactionOut(BaseModel):
    id: int
    user_id: int
    bank_account_id: Optional[int]
    date: str
    merchant: str
    amount: float
    type: str
    category: str
    payment_method: str
    notes: Optional[str]
    is_recurring: bool
    confidence_score: float
    categorizer_type: str
    created_at: datetime

    class Config:
        from_attributes = True

class TransactionFilter(BaseModel):
    search: Optional[str] = None
    category: Optional[str] = None
    type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    bank_account_id: Optional[int] = None
    page: int = 1
    limit: int = 20
    sort_by: str = "date"
    sort_order: str = "desc"

class PaginatedTransactions(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    items: List[TransactionOut]

class CSVUploadSummary(BaseModel):
    total_rows: int
    success_count: int
    failed_count: int
    added_transactions: List[TransactionOut]
    categorization_breakdown: Dict[str, int]

# --- Budget Schemas ---
class BudgetCreate(BaseModel):
    category: str
    period: str = "Monthly"
    amount: float
    alert_threshold: float = 0.8

class BudgetOut(BaseModel):
    id: int
    category: str
    period: str
    amount: float
    spent_amount: float = 0.0
    remaining_amount: float = 0.0
    percentage_used: float = 0.0
    status: str = "OK"  # OK, WARNING, OVERSPENT
    alert_threshold: float
    created_at: datetime

    class Config:
        from_attributes = True

# --- Goal Schemas ---
class GoalCreate(BaseModel):
    title: str
    category: str = "Savings"
    target_amount: float
    current_amount: float = 0.0
    deadline: str  # YYYY-MM-DD

class GoalOut(BaseModel):
    id: int
    title: str
    category: str
    target_amount: float
    current_amount: float
    deadline: str
    progress_percentage: float
    expected_completion_date: str
    ai_monthly_saving_suggestion: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class GoalContribution(BaseModel):
    amount: float

# --- Analytics Schemas ---
class DashboardOverview(BaseModel):
    total_income: float
    total_expense: float
    savings: float
    current_balance: float
    savings_rate: float
    recent_transactions: List[TransactionOut]
    monthly_cash_flow: List[Dict[str, Any]]
    category_distribution: List[Dict[str, Any]]

class ExpenseAnalyticsOut(BaseModel):
    category_wise: List[Dict[str, Any]]
    top_merchants: List[Dict[str, Any]]
    recurring_expenses: List[Dict[str, Any]]
    weekend_spending: Dict[str, Any]
    heatmap: List[Dict[str, Any]]
    income_vs_expense_trend: List[Dict[str, Any]]

# --- Health Score & Savings Engine ---
class HealthScoreOut(BaseModel):
    score: int
    rating: str  # Excellent, Good, Average, Poor
    metrics: Dict[str, Any]
    improvements: List[str]

class SavingsRecommendationOut(BaseModel):
    total_potential_savings: float
    recommendations: List[Dict[str, Any]]

# --- Forecast & EMI Schemas ---
class ForecastOut(BaseModel):
    next_month_spending: float
    future_savings: float
    category_forecast: List[Dict[str, Any]]
    cash_flow_forecast: List[Dict[str, Any]]
    confidence: float
    method: str

class EMICalculationRequest(BaseModel):
    loan_amount: float
    interest_rate: float  # annual %
    tenure_months: int

class EMICalculationResult(BaseModel):
    monthly_emi: float
    total_interest: float
    total_payment: float
    schedule: List[Dict[str, Any]]
    comparison: List[Dict[str, Any]]

# --- Chatbot & Education ---
class ChatMessageRequest(BaseModel):
    message: str

class ChatResponseOut(BaseModel):
    response: str
    suggested_actions: Optional[List[str]] = None
    created_at: datetime

class InvestmentEducationTopicOut(BaseModel):
    topic_id: str
    title: str
    definition: str
    benefits: List[str]
    risks: List[str]
    examples: List[str]
    beginner_tips: List[str]
    learning_resources: List[Dict[str, str]]
    faqs: List[Dict[str, str]]

class AISuggestionOut(BaseModel):
    topic_id: str
    user_context_summary: str
    educational_suggestions: List[str]
    suggested_learning_investment: float
    disclaimer: str

# --- Notifications ---
class NotificationOut(BaseModel):
    id: int
    type: str
    title: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
