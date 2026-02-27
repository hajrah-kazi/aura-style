from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..services.recommendation_service import RecommendationService
from ..schemas.schemas import ProductOut
from .auth import get_current_user
from ..models import models

router = APIRouter()

@router.get("/personalized", response_model=List[ProductOut])
def get_personalized_recommendations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return RecommendationService.get_personalized_recommendations(db, user_id=current_user.id)

@router.get("/similar/{product_id}", response_model=List[ProductOut])
def get_similar_products(
    product_id: int,
    db: Session = Depends(get_db)
):
    return RecommendationService.get_contextual_recommendations(db, product_id=product_id)

@router.get("/trending", response_model=List[ProductOut])
def get_trending_products(db: Session = Depends(get_db)):
    return RecommendationService.get_trending_recommendations(db)

@router.post("/rebuild", tags=["Admin"])
def rebuild_model(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Only admin should do this usually (simplified for demo)
    return RecommendationService.trigger_rebuild(db)
