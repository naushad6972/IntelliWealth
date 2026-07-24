from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.models import User, BankAccount, BankConsent, Transaction, SyncLog
from app.schemas.schemas import (
    BankAccountOut, BankConsentInitiateRequest, BankConsentInitiateResponse,
    BankConsentCallbackRequest
)
from app.core.deps import get_current_user
from app.services.bank_integration.factory import BankProviderFactory

router = APIRouter(prefix="/banks", tags=["Bank Integration"])

@router.get("/providers")
def get_bank_providers(current_user: User = Depends(get_current_user)):
    return BankProviderFactory.list_providers()

@router.post("/connect/initiate", response_model=BankConsentInitiateResponse)
def initiate_bank_connection(
    req: BankConsentInitiateRequest,
    current_user: User = Depends(get_current_user)
):
    adapter = BankProviderFactory.get_adapter(req.provider_id)
    redirect_url, consent_id = adapter.initiate_consent(
        user_id=current_user.id,
        bank_name=req.bank_name,
        account_type=req.account_type or "Savings"
    )
    return BankConsentInitiateResponse(
        redirect_url=redirect_url,
        consent_id=consent_id,
        provider_id=req.provider_id,
        message=f"OAuth consent initiated for {req.bank_name} via {adapter.provider_name}."
    )

@router.post("/connect/callback", response_model=BankAccountOut)
def process_bank_callback(
    req: BankConsentCallbackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    adapter = BankProviderFactory.get_adapter(req.provider_id)
    token_resp = adapter.exchange_code_for_token(req.consent_id, req.code)

    # Fetch accounts from bank provider adapter
    accounts_data = adapter.fetch_accounts(token_resp["access_token"])
    if not accounts_data:
        raise HTTPException(status_code=400, detail="No bank accounts found for this consent.")

    primary_acc_data = accounts_data[0]
    
    # Create or update BankAccount
    bank_acc = BankAccount(
        user_id=current_user.id,
        provider_id=req.provider_id,
        bank_name=primary_acc_data["bank_name"],
        account_number_masked=primary_acc_data["account_number_masked"],
        account_type=primary_acc_data["account_type"],
        currency=primary_acc_data["currency"],
        balance=primary_acc_data["balance"],
        status="ACTIVE",
        auto_sync=True,
        last_synced_at=datetime.utcnow()
    )
    db.add(bank_acc)
    db.flush()

    # Create BankConsent
    expires_sec = token_resp.get("expires_in_seconds", 3600 * 24 * 30)
    consent = BankConsent(
        user_id=current_user.id,
        bank_account_id=bank_acc.id,
        provider_type=req.provider_id,
        consent_id=req.consent_id,
        access_token=token_resp["access_token"],
        refresh_token=token_resp.get("refresh_token"),
        token_expires_at=datetime.utcnow() + timedelta(seconds=expires_sec),
        status="GRANTED"
    )
    db.add(consent)

    # Immediate initial transaction sync
    raw_txs = adapter.fetch_transactions(token_resp["access_token"], bank_acc.account_number_masked)
    added_count = 0
    for tx_data in raw_txs:
        tx = Transaction(
            user_id=current_user.id,
            bank_account_id=bank_acc.id,
            date=tx_data["date"],
            merchant=tx_data["merchant"],
            amount=tx_data["amount"],
            type=tx_data.get("type", "Expense"),
            category=tx_data.get("category", "Miscellaneous"),
            payment_method=tx_data.get("payment_method", "UPI/Bank"),
            raw_description=tx_data.get("raw_description", ""),
            categorizer_type="BANK_SYNC"
        )
        db.add(tx)
        added_count += 1

    sync_log = SyncLog(
        user_id=current_user.id,
        bank_account_id=bank_acc.id,
        sync_type="INITIAL_CONNECT",
        status="SUCCESS",
        transactions_added=added_count
    )
    db.add(sync_log)

    db.commit()
    db.refresh(bank_acc)
    return bank_acc

@router.get("/accounts", response_model=List[BankAccountOut])
def get_user_bank_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    accounts = db.query(BankAccount).filter(BankAccount.user_id == current_user.id).all()
    return accounts

@router.post("/accounts/{account_id}/sync", response_model=BankAccountOut)
def sync_bank_account_manual(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = db.query(BankAccount).filter(
        BankAccount.id == account_id,
        BankAccount.user_id == current_user.id
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Bank account not found.")

    consent = db.query(BankConsent).filter(
        BankConsent.bank_account_id == account.id,
        BankConsent.status == "GRANTED"
    ).first()

    if not consent:
        raise HTTPException(status_code=400, detail="Bank consent missing or expired.")

    adapter = BankProviderFactory.get_adapter(account.provider_id)
    raw_txs = adapter.fetch_transactions(consent.access_token, account.account_number_masked)

    added_count = 0
    for tx_data in raw_txs:
        existing = db.query(Transaction).filter(
            Transaction.user_id == current_user.id,
            Transaction.bank_account_id == account.id,
            Transaction.date == tx_data["date"],
            Transaction.merchant == tx_data["merchant"],
            Transaction.amount == tx_data["amount"]
        ).first()

        if not existing:
            tx = Transaction(
                user_id=current_user.id,
                bank_account_id=account.id,
                date=tx_data["date"],
                merchant=tx_data["merchant"],
                amount=tx_data["amount"],
                type=tx_data.get("type", "Expense"),
                category=tx_data.get("category", "Miscellaneous"),
                payment_method=tx_data.get("payment_method", "UPI/Bank"),
                raw_description=tx_data.get("raw_description", ""),
                categorizer_type="MANUAL_SYNC"
            )
            db.add(tx)
            added_count += 1

    account.last_synced_at = datetime.utcnow()
    sync_log = SyncLog(
        user_id=current_user.id,
        bank_account_id=account.id,
        sync_type="MANUAL",
        status="SUCCESS",
        transactions_added=added_count
    )
    db.add(sync_log)

    db.commit()
    db.refresh(account)
    return account

@router.delete("/accounts/{account_id}")
def disconnect_bank_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = db.query(BankAccount).filter(
        BankAccount.id == account_id,
        BankAccount.user_id == current_user.id
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Bank account not found.")

    consent = db.query(BankConsent).filter(BankConsent.bank_account_id == account.id).first()
    if consent:
        adapter = BankProviderFactory.get_adapter(account.provider_id)
        try:
            adapter.revoke_consent(consent.consent_id, consent.access_token)
        except Exception:
            pass
        db.delete(consent)

    db.delete(account)
    db.commit()
    return {"message": "Bank account disconnected and consent revoked successfully."}
