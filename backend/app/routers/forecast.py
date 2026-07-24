from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User
from app.schemas.schemas import ForecastOut
from app.core.deps import get_current_user
from app.ml.forecaster import predict_future_spending

router = APIRouter(prefix="/forecast", tags=["Spending Forecast"])

@router.get("/predict", response_model=ForecastOut)
def get_spending_forecast(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    res = predict_future_spending(db, current_user)
    return ForecastOut(
        next_month_spending=res["next_month_spending"],
        future_savings=res["future_savings"],
        category_forecast=res["category_forecast"],
        cash_flow_forecast=res["cash_flow_forecast"],
        confidence=res["confidence"],
        method=res["method"]
    )
