from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from typing import Optional, List, Dict
import math

from app.db.session import get_db
from app.models.models import User, Transaction, BankAccount
from app.schemas.schemas import (
    TransactionCreate, TransactionUpdate, TransactionOut, PaginatedTransactions, CSVUploadSummary
)
from app.core.deps import get_current_user
from app.ml.categorizer import categorizer_engine
from app.services.csv_service import parse_bank_csv

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("", response_model=PaginatedTransactions)
def list_transactions(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    bank_account_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("date"),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)

    if search:
        s = f"%{search}%"
        query = query.filter(or_(Transaction.merchant.ilike(s), Transaction.notes.ilike(s), Transaction.category.ilike(s)))
    if category:
        query = query.filter(Transaction.category == category)
    if type:
        query = query.filter(Transaction.type == type)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    if bank_account_id:
        query = query.filter(Transaction.bank_account_id == bank_account_id)

    # Sorting
    sort_col = getattr(Transaction, sort_by, Transaction.date)
    if sort_order.lower() == "asc":
        query = query.order_by(asc(sort_col))
    else:
        query = query.order_by(desc(sort_col))

    total = query.count()
    total_pages = math.ceil(total / limit) if total > 0 else 1
    items = query.offset((page - 1) * limit).limit(limit).all()

    return PaginatedTransactions(
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
        items=items
    )

@router.post("", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(
    tx_in: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Auto categorization if category is blank
    if not tx_in.category or tx_in.category.strip() == "":
        category, confidence, cat_type = categorizer_engine.categorize(tx_in.merchant, amount=tx_in.amount)
    else:
        category = tx_in.category
        confidence = 1.0
        cat_type = "MANUAL"

    tx = Transaction(
        user_id=current_user.id,
        bank_account_id=tx_in.bank_account_id,
        date=tx_in.date,
        merchant=tx_in.merchant,
        amount=tx_in.amount,
        type=tx_in.type,
        category=category,
        payment_method=tx_in.payment_method or "UPI/Bank",
        notes=tx_in.notes,
        confidence_score=confidence,
        categorizer_type=cat_type
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

@router.put("/{tx_id}", response_model=TransactionOut)
def update_transaction(
    tx_id: int,
    tx_in: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tx = db.query(Transaction).filter(Transaction.id == tx_id, Transaction.user_id == current_user.id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found.")

    if tx_in.date is not None:
        tx.date = tx_in.date
    if tx_in.merchant is not None:
        tx.merchant = tx_in.merchant
    if tx_in.amount is not None:
        tx.amount = tx_in.amount
    if tx_in.type is not None:
        tx.type = tx_in.type
    if tx_in.category is not None:
        tx.category = tx_in.category
        tx.categorizer_type = "MANUAL_EDIT"
    if tx_in.payment_method is not None:
        tx.payment_method = tx_in.payment_method
    if tx_in.notes is not None:
        tx.notes = tx_in.notes

    db.commit()
    db.refresh(tx)
    return tx

@router.delete("/{tx_id}")
def delete_transaction(
    tx_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tx = db.query(Transaction).filter(Transaction.id == tx_id, Transaction.user_id == current_user.id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    db.delete(tx)
    db.commit()
    return {"message": "Transaction deleted successfully."}

@router.post("/upload-csv", response_model=CSVUploadSummary)
async def upload_csv_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are supported.")

    file_bytes = await file.read()
    try:
        raw_transactions = parse_bank_csv(file_bytes, file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV file: {str(e)}")

    added_txs = []
    cat_breakdown: Dict[str, int] = {}

    for tx_data in raw_transactions:
        tx = Transaction(
            user_id=current_user.id,
            date=tx_data["date"],
            merchant=tx_data["merchant"],
            amount=tx_data["amount"],
            type=tx_data["type"],
            category=tx_data["category"],
            payment_method=tx_data["payment_method"],
            notes=tx_data["notes"],
            confidence_score=tx_data["confidence_score"],
            categorizer_type=tx_data["categorizer_type"]
        )
        db.add(tx)
        added_txs.append(tx)

        cat = tx_data["category"]
        cat_breakdown[cat] = cat_breakdown.get(cat, 0) + 1

    db.commit()
    for t in added_txs:
        db.refresh(t)

    return CSVUploadSummary(
        total_rows=len(raw_transactions),
        success_count=len(added_txs),
        failed_count=0,
        added_transactions=[TransactionOut.model_validate(t) for t in added_txs],
        categorization_breakdown=cat_breakdown
    )
