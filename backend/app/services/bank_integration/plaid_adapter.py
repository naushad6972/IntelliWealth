import uuid
from typing import Dict, Any, List, Optional, Tuple
from app.services.bank_integration.base_adapter import BankProviderAdapter

class PlaidAdapter(BankProviderAdapter):
    """
    Plaid Global Financial Aggregator Adapter.
    """
    @property
    def provider_id(self) -> str:
        return "plaid"

    @property
    def provider_name(self) -> str:
        return "Plaid Financial Aggregator"

    def initiate_consent(self, user_id: int, bank_name: str, account_type: str = "Savings") -> Tuple[str, str]:
        consent_id = f"plaid_link_token_{uuid.uuid4().hex[:14]}"
        redirect_url = f"/bank/callback?provider=plaid&consent_id={consent_id}&code=public_token_{uuid.uuid4().hex[:8]}"
        return redirect_url, consent_id

    def exchange_code_for_token(self, consent_id: str, code: str) -> Dict[str, Any]:
        return {
            "access_token": f"access-sandbox-{uuid.uuid4().hex}",
            "refresh_token": f"refresh-sandbox-{uuid.uuid4().hex}",
            "expires_in_seconds": 3600 * 24 * 180
        }

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        return {
            "access_token": f"access-sandbox-refreshed-{uuid.uuid4().hex[:10]}",
            "refresh_token": refresh_token,
            "expires_in_seconds": 3600 * 24 * 180
        }

    def fetch_accounts(self, access_token: str) -> List[Dict[str, Any]]:
        return [
            {
                "bank_name": "Citibank Plaid Linked",
                "account_number_masked": "**** 1109",
                "account_type": "Checking",
                "currency": "INR",
                "balance": 94200.00
            }
        ]

    def fetch_transactions(self, access_token: str, account_masked_id: str, since_date: Optional[str] = None) -> List[Dict[str, Any]]:
        return [
            {
                "date": "2026-07-23",
                "merchant": "Uber Eats",
                "amount": 340.0,
                "type": "Expense",
                "raw_description": "PLAID/UBER-EATS/SAN-FRAN",
                "category": "Food",
                "payment_method": "Credit Card"
            }
        ]

    def revoke_consent(self, consent_id: str, access_token: str) -> bool:
        return True
