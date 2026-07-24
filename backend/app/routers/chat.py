from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.session import get_db
from app.models.models import User, ChatHistory
from app.schemas.schemas import ChatMessageRequest, ChatResponseOut
from app.core.deps import get_current_user
from app.services.ai_service import AIService

router = APIRouter(prefix="/chat", tags=["AI Financial Chatbot"])

@router.post("", response_model=ChatResponseOut)
def send_chat_message(
    req: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Save user message to history
    user_chat = ChatHistory(
        user_id=current_user.id,
        role="user",
        content=req.message
    )
    db.add(user_chat)
    db.flush()

    # Process query
    ai_res = AIService.process_chat_message(db, current_user, req.message)

    # Save assistant response to history
    asst_chat = ChatHistory(
        user_id=current_user.id,
        role="assistant",
        content=ai_res["response"]
    )
    db.add(asst_chat)
    db.commit()

    return ChatResponseOut(
        response=ai_res["response"],
        suggested_actions=ai_res["suggested_actions"],
        created_at=datetime.utcnow()
    )

@router.get("/history")
def get_chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history = db.query(ChatHistory).filter(
        ChatHistory.user_id == current_user.id
    ).order_by(ChatHistory.created_at.asc()).all()

    return [
        {
            "id": h.id,
            "role": h.role,
            "content": h.content,
            "created_at": h.created_at
        }
        for h in history
    ]
