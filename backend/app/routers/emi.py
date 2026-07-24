from fastapi import APIRouter
from typing import List, Dict, Any
import math

from app.schemas.schemas import EMICalculationRequest, EMICalculationResult

router = APIRouter(prefix="/emi", tags=["EMI Calculator"])

@router.post("/calculate", response_model=EMICalculationResult)
def calculate_emi(req: EMICalculationRequest):
    P = req.loan_amount
    R = req.interest_rate
    n = req.tenure_months

    if P <= 0 or n <= 0:
        return EMICalculationResult(
            monthly_emi=0.0,
            total_interest=0.0,
            total_payment=0.0,
            schedule=[],
            comparison=[]
        )

    r = (R / 12) / 100.0
    if r > 0:
        emi = P * r * (math.pow(1 + r, n)) / (math.pow(1 + r, n) - 1)
    else:
        emi = P / n

    total_payment = emi * n
    total_interest = total_payment - P

    # Amortization Schedule
    schedule = []
    balance = P
    for month in range(1, n + 1):
        interest_paid = balance * r
        principal_paid = emi - interest_paid
        balance = max(0.0, balance - principal_paid)

        schedule.append({
            "month": month,
            "emi": round(emi, 2),
            "principal_paid": round(principal_paid, 2),
            "interest_paid": round(interest_paid, 2),
            "balance": round(balance, 2)
        })

    # Loan Comparisons for different tenures
    comparison = []
    for test_tenure in [12, 24, 36, 60, 120, 240]:
        if test_tenure == n:
            test_emi = emi
        else:
            test_r = (R / 12) / 100.0
            test_emi = P * test_r * (math.pow(1 + test_r, test_tenure)) / (math.pow(1 + test_r, test_tenure) - 1)
        test_total = test_emi * test_tenure
        comparison.append({
            "tenure_months": test_tenure,
            "tenure_years": round(test_tenure / 12, 1),
            "monthly_emi": round(test_emi, 2),
            "total_interest": round(test_total - P, 2),
            "total_payment": round(test_total, 2)
        })

    return EMICalculationResult(
        monthly_emi=round(emi, 2),
        total_interest=round(total_interest, 2),
        total_payment=round(total_payment, 2),
        schedule=schedule,
        comparison=comparison
    )
