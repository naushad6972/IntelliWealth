from typing import Dict
from app.services.bank_integration.base_adapter import BankProviderAdapter
from app.services.bank_integration.mock_adapter import MockProviderAdapter
from app.services.bank_integration.open_banking import OpenBankingAdapter
from app.services.bank_integration.account_aggregator import AccountAggregatorAdapter
from app.services.bank_integration.plaid_adapter import PlaidAdapter

class BankProviderFactory:
    _adapters: Dict[str, BankProviderAdapter] = {
        "mock": MockProviderAdapter(),
        "open_banking": OpenBankingAdapter(),
        "account_aggregator": AccountAggregatorAdapter(),
        "plaid": PlaidAdapter()
    }

    @classmethod
    def get_adapter(cls, provider_id: str) -> BankProviderAdapter:
        adapter = cls._adapters.get(provider_id.lower())
        if not adapter:
            # Fallback to mock adapter if unknown provider specified
            return cls._adapters["mock"]
        return adapter

    @classmethod
    def list_providers(cls):
        return [
            {"id": k, "name": v.provider_name}
            for k, v in cls._adapters.items()
        ]
