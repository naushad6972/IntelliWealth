from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

class BankProviderAdapter(ABC):
    @property
    @abstractmethod
    def provider_id(self) -> str:
        """Returns unique provider identifier (e.g. 'open_banking', 'account_aggregator', 'plaid', 'mock')"""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Returns human readable provider name"""
        pass

    @abstractmethod
    def initiate_consent(self, user_id: int, bank_name: str, account_type: str = "Savings") -> Tuple[str, str]:
        """
        Initiates OAuth/Consent flow.
        Returns (redirect_url, consent_id)
        """
        pass

    @abstractmethod
    def exchange_code_for_token(self, consent_id: str, code: str) -> Dict[str, Any]:
        """
        Exchanges authorization code / consent handle for tokens.
        Returns dict containing: access_token, refresh_token, expires_in_seconds
        """
        pass

    @abstractmethod
    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refreshes expired access token.
        Returns dict containing: access_token, refresh_token, expires_in_seconds
        """
        pass

    @abstractmethod
    def fetch_accounts(self, access_token: str) -> List[Dict[str, Any]]:
        """
        Fetches list of bank accounts tied to access token.
        Returns list of dicts: bank_name, account_number_masked, account_type, currency, balance
        """
        pass

    @abstractmethod
    def fetch_transactions(self, access_token: str, account_masked_id: str, since_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetches transactions for an account.
        Returns list of dicts: date, merchant, amount, type, raw_description, category
        """
        pass

    @abstractmethod
    def revoke_consent(self, consent_id: str, access_token: str) -> bool:
        """
        Revokes existing consent / token.
        """
        pass
