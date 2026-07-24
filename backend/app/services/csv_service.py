import pandas as pd
import io
from typing import List, Dict, Any, Tuple
from app.ml.categorizer import categorizer_engine

def parse_bank_csv(file_bytes: bytes, filename: str) -> List[Dict[str, Any]]:
    """
    Parses CSV content from various bank formats (HDFC, SBI, ICICI, Chase, Generic CSVs).
    Auto-detects date, merchant, amount, type, and category columns.
    """
    df = pd.read_csv(io.BytesIO(file_bytes))
    
    # Normalize column headers
    cols = [str(c).strip().lower() for c in df.columns]
    df.columns = cols

    date_col = next((c for c in cols if any(k in c for k in ["date", "txn date", "transaction date", "time"])), None)
    merchant_col = next((c for c in cols if any(k in c for k in ["merchant", "description", "narration", "payee", "particulars", "details"])), None)
    amount_col = next((c for c in cols if any(k in c for k in ["amount", "txn amount", "value", "sum"])), None)
    debit_col = next((c for c in cols if any(k in c for k in ["debit", "withdrawal", "spent"])), None)
    credit_col = next((c for c in cols if any(k in c for k in ["credit", "deposit", "received"])), None)
    category_col = next((c for c in cols if "category" in c), None)

    transactions = []
    
    for idx, row in df.iterrows():
        date_val = str(row[date_col]).strip() if date_col and pd.notna(row[date_col]) else "2026-07-24"
        merchant_val = str(row[merchant_col]).strip() if merchant_col and pd.notna(row[merchant_col]) else "Unknown Merchant"
        
        # Determine amount and type
        amt = 0.0
        tx_type = "Expense"
        
        if amount_col and pd.notna(row[amount_col]):
            try:
                amt = float(str(row[amount_col]).replace(",", "").replace("$", "").replace("₹", ""))
                if amt < 0:
                    amt = abs(amt)
                    tx_type = "Expense"
                elif "type" in cols and pd.notna(row["type"]):
                    tx_type = str(row["type"]).strip().title()
            except ValueError:
                amt = 0.0
        elif debit_col or credit_col:
            d_val = float(str(row[debit_col]).replace(",", "")) if debit_col and pd.notna(row[debit_col]) and str(row[debit_col]).strip() != "" else 0.0
            c_val = float(str(row[credit_col]).replace(",", "")) if credit_col and pd.notna(row[credit_col]) and str(row[credit_col]).strip() != "" else 0.0
            if c_val > 0:
                amt = c_val
                tx_type = "Income"
            else:
                amt = d_val
                tx_type = "Expense"

        if amt <= 0:
            continue

        # AI Auto-Categorization if category not present
        if category_col and pd.notna(row[category_col]) and str(row[category_col]).strip() != "":
            cat_val = str(row[category_col]).strip().title()
            confidence = 1.0
            cat_type = "CSV_EXPLICIT"
        else:
            cat_val, confidence, cat_type = categorizer_engine.categorize(merchant_val, raw_description=merchant_val, amount=amt)

        transactions.append({
            "date": date_val,
            "merchant": merchant_val,
            "amount": round(amt, 2),
            "type": tx_type,
            "category": cat_val,
            "payment_method": "CSV Import",
            "notes": f"Uploaded from {filename}",
            "confidence_score": confidence,
            "categorizer_type": cat_type
        })

    return transactions
