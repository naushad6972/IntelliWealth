import uuid
from typing import Dict, Any, List, Optional, Tuple
from app.services.bank_integration.base_adapter import BankProviderAdapter

class AccountAggregatorAdapter(BankProviderAdapter):
    """
    India Account Aggregator (AA) Architecture Adapter (ReBIT Specs).
    FIU (Financial Information User) to AA Handle consent handshake and encrypted FI payload retrieval.
    """
    @property
    def provider_id(self) -> str:
        return "account_aggregator"

    @property
    def provider_name(self) -> str:
        return "Account Aggregator India (OnOneMoney / Finvu / Anumati)"

    def initiate_consent(self, user_id: int, bank_name: str, account_type: str = "Savings") -> Tuple[str, str]:
        consent_id = f"aa_consent_handle_{uuid.uuid4().hex[:14]}"
        redirect_url = f"/bank/callback?provider=account_aggregator&consent_id={consent_id}&code=aa_approval_session_{uuid.uuid4().hex[:8]}"
        return redirect_url, consent_id

    def exchange_code_for_token(self, consent_id: str, code: str) -> Dict[str, Any]:
        return {
            "access_token": f"aa_fi_session_token_{uuid.uuid4().hex}",
            "refresh_token": f"aa_consent_refresh_token_{uuid.uuid4().hex}",
            "expires_in_seconds": 3600 * 24 * 365  # 1 year AA consent artifact default
        }

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        return {
            "access_token": f"aa_fi_session_token_refreshed_{uuid.uuid4().hex[:10]}",
            "refresh_token": refresh_token,
            "expires_in_seconds": 3600 * 24 * 365
        }

    def fetch_accounts(self, access_token: str) -> List[Dict[str, Any]]:
        return [
            {
                "bank_name": "State Bank of India (AA Linked)",
                "account_number_masked": "**** 3391",
                "account_type": "Savings",
                "currency": "INR",
                "balance": 215000.00
            },
            {
                "bank_name": "Axis Bank (AA Linked)",
                "account_number_masked": "**** 6104",
                "account_type": "Savings",
                "currency": "INR",
                "balance": 87500.00
            }
        ]

    def fetch_transactions(self, access_token: str, account_masked_id: str, since_date: Optional[str] = None) -> List[Dict[str, Any]]:
        return [
            {
                "date": "2026-07-22",
                "merchant": "Mutual Fund SIP Nippon India",
                "amount": 5000.0,
                "type": "Expense",
                "raw_description": "ACH/NIPPON-INDIA-MF/SIP",
                "category": "Investment",
                "payment_method": "Bank Transfer"
            },
            {
                "date": "2026-07-21",
                "merchant": "Zomato Online Food",
                "amount": 520.0,
                "type": "Expense",
                "raw_description": "UPI/ZOMATO/PAYMENT",
                "category": "Food",
                "payment_method": "UPI/Bank"
            }
        ]

    def revoke_consent(self, consent_id: str, access_token: str) -> bool:
        return True
