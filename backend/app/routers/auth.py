from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User
from app.schemas.schemas import UserRegister, UserLogin, Token, UserProfile, UserProfileUpdate
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    user = User(
        name=user_in.name,
        email=user_in.email.lower(),
        hashed_password=get_password_hash(user_in.password),
        monthly_income=user_in.monthly_income or 50000.0,
        occupation=user_in.occupation or "Professional",
        risk_preference=user_in.risk_preference or "Moderate",
        financial_goals=user_in.financial_goals or "Emergency Fund & Wealth Growth",
        preferred_currency=user_in.preferred_currency or "INR"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserProfile.model_validate(user)
    }

@router.post("/login", response_model=Token)
def login_user(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserProfile.model_validate(user)
    }

@router.get("/me", response_model=UserProfile)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserProfile)
def update_profile(
    profile_in: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if profile_in.name is not None:
        current_user.name = profile_in.name
    if profile_in.monthly_income is not None:
        current_user.monthly_income = profile_in.monthly_income
    if profile_in.occupation is not None:
        current_user.occupation = profile_in.occupation
    if profile_in.risk_preference is not None:
        current_user.risk_preference = profile_in.risk_preference
    if profile_in.financial_goals is not None:
        current_user.financial_goals = profile_in.financial_goals
    if profile_in.preferred_currency is not None:
        current_user.preferred_currency = profile_in.preferred_currency

    db.commit()
    db.refresh(current_user)
    return current_user
