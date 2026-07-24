from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.models import User
from app.schemas.schemas import InvestmentEducationTopicOut, AISuggestionOut
from app.core.deps import get_current_user
from app.services.education_data import INVESTMENT_TOPICS
from app.services.ai_service import AIService

router = APIRouter(prefix="/education", tags=["Investment Education"])

@router.get("/topics", response_model=List[InvestmentEducationTopicOut])
def list_education_topics():
    return [InvestmentEducationTopicOut(**data) for data in INVESTMENT_TOPICS.values()]

@router.get("/topics/{topic_id}", response_model=InvestmentEducationTopicOut)
def get_education_topic(topic_id: str):
    topic = INVESTMENT_TOPICS.get(topic_id.lower())
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found.")
    return InvestmentEducationTopicOut(**topic)

@router.get("/topics/{topic_id}/suggestions", response_model=AISuggestionOut)
def get_ai_investment_suggestions(
    topic_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    topic = INVESTMENT_TOPICS.get(topic_id.lower())
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found.")

    res = AIService.generate_educational_investment_suggestions(db, current_user, topic_id)
    return AISuggestionOut(**res)
