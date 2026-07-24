import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from app.services.bank_integration.base_adapter import BankProviderAdapter

class MockProviderAdapter(BankProviderAdapter):
    @property
    def provider_id(self) -> str:
        return "mock"

    @property
    def provider_name(self) -> str:
        return "Mock Bank Direct Sync Adapter"

    def initiate_consent(self, user_id: int, bank_name: str, account_type: str = "Savings") -> Tuple[str, str]:
        consent_id = f"mock_consent_{uuid.uuid4().hex[:12]}"
        # Direct OAuth simulation callback URL
        redirect_url = f"/bank/callback?provider=mock&consent_id={consent_id}&code=auth_code_sim_{uuid.uuid4().hex[:8]}"
        return redirect_url, consent_id

    def exchange_code_for_token(self, consent_id: str, code: str) -> Dict[str, Any]:
        return {
            "access_token": f"mock_access_{uuid.uuid4().hex}",
            "refresh_token": f"mock_refresh_{uuid.uuid4().hex}",
            "expires_in_seconds": 3600 * 24 * 30  # 30 days
        }

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        return {
            "access_token": f"mock_access_refreshed_{uuid.uuid4().hex[:12]}",
            "refresh_token": refresh_token,
            "expires_in_seconds": 3600 * 24 * 30
        }

    def fetch_accounts(self, access_token: str) -> List[Dict[str, Any]]:
        return [
            {
                "bank_name": "HDFC Premium Banking",
                "account_number_masked": "**** 4829",
                "account_type": "Savings",
                "currency": "INR",
                "balance": 184500.00
            },
            {
                "bank_name": "ICICI Wealth Management",
                "account_number_masked": "**** 9102",
                "account_type": "Checking",
                "currency": "INR",
                "balance": 45200.50
            }
        ]

    def fetch_transactions(self, access_token: str, account_masked_id: str, since_date: Optional[str] = None) -> List[Dict[str, Any]]:
        today = datetime.now()
        sample_merchants = [
            ("Swiggy Food", 450.0, "Expense", "Food"),
            ("Uber Trip", 320.0, "Expense", "Travel"),
            ("Amazon Shopping", 2499.0, "Expense", "Shopping"),
            ("Netflix Subscription", 649.0, "Expense", "Entertainment"),
            ("Electricity Bill Payment", 1850.0, "Expense", "Bills"),
            ("Salary Credit Acme Corp", 95000.0, "Income", "Salary"),
            ("HPCL Fuel Station", 1500.0, "Expense", "Fuel"),
            ("Zerodha Investment SIP", 10000.0, "Expense", "Investment"),
            ("Apollo Pharmacy", 850.0, "Expense", "Healthcare"),
            ("Starbucks Coffee", 380.0, "Expense", "Food"),
            ("DMart Supermarket", 3400.0, "Expense", "Food")
        ]

        txs = []
        for i in range(12):
            tx_date = (today - timedelta(days=i * 2 + random.randint(0, 1))).strftime("%Y-%m-%d")
            merchant, base_amt, tx_type, category = random.choice(sample_merchants)
            # Add subtle jitter
            amt = round(base_amt + (random.randint(-20, 50) if tx_type == "Expense" else 0), 2)
            txs.append({
                "date": tx_date,
                "merchant": merchant,
                "amount": amt,
                "type": tx_type,
                "raw_description": f"UPI/{merchant.upper()}/REF-{random.randint(100000, 999999)}",
                "category": category,
                "payment_method": "UPI/Bank"
            })
        return txs

    def revoke_consent(self, consent_id: str, access_token: str) -> bool:
        return True
