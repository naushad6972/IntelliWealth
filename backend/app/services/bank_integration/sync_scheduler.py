import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.models import BankAccount, BankConsent, Transaction, SyncLog
from app.services.bank_integration.factory import BankProviderFactory

logger = logging.getLogger(__name__)

def perform_background_bank_sync():
    """
    Background worker loop that scans active bank accounts with consents,
    refreshes expired access tokens via provider adapters, pulls new transactions,
    and logs sync status.
    """
    db: Session = SessionLocal()
    try:
        active_accounts = db.query(BankAccount).filter(
            BankAccount.status == "ACTIVE",
            BankAccount.auto_sync == True
        ).all()

        for account in active_accounts:
            consent = db.query(BankConsent).filter(
                BankConsent.bank_account_id == account.id,
                BankConsent.status == "GRANTED"
            ).first()

            if not consent:
                continue

            adapter = BankProviderFactory.get_adapter(account.provider_id)
            
            # Check token expiration
            if consent.token_expires_at and consent.token_expires_at <= datetime.utcnow():
                try:
                    refreshed = adapter.refresh_token(consent.refresh_token)
                    consent.access_token = refreshed["access_token"]
                    if "refresh_token" in refreshed:
                        consent.refresh_token = refreshed["refresh_token"]
                    consent.token_expires_at = datetime.utcnow() + timedelta(seconds=refreshed.get("expires_in_seconds", 86400))
                    consent.updated_at = datetime.utcnow()
                    db.commit()
                except Exception as e:
                    logger.error(f"Token refresh failed for consent {consent.id}: {e}")
                    consent.status = "EXPIRED"
                    db.commit()
                    continue

            # Sync transactions
            try:
                raw_txs = adapter.fetch_transactions(
                    access_token=consent.access_token,
                    account_masked_id=account.account_number_masked,
                    since_date=account.last_synced_at.strftime("%Y-%m-%d") if account.last_synced_at else None
                )

                added_count = 0
                for tx_data in raw_txs:
                    # Deduplicate by merchant, date, and amount for user
                    existing = db.query(Transaction).filter(
                        Transaction.user_id == account.user_id,
                        Transaction.bank_account_id == account.id,
                        Transaction.date == tx_data["date"],
                        Transaction.merchant == tx_data["merchant"],
                        Transaction.amount == tx_data["amount"]
                    ).first()

                    if not existing:
                        new_tx = Transaction(
                            user_id=account.user_id,
                            bank_account_id=account.id,
                            date=tx_data["date"],
                            merchant=tx_data["merchant"],
                            amount=tx_data["amount"],
                            type=tx_data.get("type", "Expense"),
                            category=tx_data.get("category", "Miscellaneous"),
                            payment_method=tx_data.get("payment_method", "UPI/Bank"),
                            raw_description=tx_data.get("raw_description", ""),
                            categorizer_type="BANK_SYNC"
                        )
                        db.add(new_tx)
                        added_count += 1

                account.last_synced_at = datetime.utcnow()
                sync_log = SyncLog(
                    user_id=account.user_id,
                    bank_account_id=account.id,
                    sync_type="AUTO_BACKGROUND",
                    status="SUCCESS",
                    transactions_added=added_count
                )
                db.add(sync_log)
                db.commit()
            except Exception as e:
                logger.error(f"Bank sync error for account {account.id}: {e}")
                sync_log = SyncLog(
                    user_id=account.user_id,
                    bank_account_id=account.id,
                    sync_type="AUTO_BACKGROUND",
                    status="FAILED",
                    error_message=str(e)
                )
                db.add(sync_log)
                db.commit()
    finally:
        db.close()
