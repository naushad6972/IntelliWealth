from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User
from app.schemas.schemas import HealthScoreOut, SavingsRecommendationOut
from app.core.deps import get_current_user
from app.ml.health_score import calculate_financial_health_score
from app.services.recommendation_engine import generate_savings_recommendations

router = APIRouter(prefix="/health", tags=["Financial Health Score"])

@router.get("/score", response_model=HealthScoreOut)
def get_health_score(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    res = calculate_financial_health_score(db, current_user)
    return HealthScoreOut(
        score=res["score"],
        rating=res["rating"],
        metrics=res["metrics"],
        improvements=res["improvements"]
    )

@router.get("/savings-recommendations", response_model=SavingsRecommendationOut)
def get_savings_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    res = generate_savings_recommendations(db, current_user)
    return SavingsRecommendationOut(
        total_potential_savings=res["total_potential_savings"],
        recommendations=res["recommendations"]
    )
