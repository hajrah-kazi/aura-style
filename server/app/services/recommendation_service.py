from sqlalchemy.orm import Session
from ..ml.engine import recommender
from ..models import models
from typing import List

class RecommendationService:
    @staticmethod
    def get_contextual_recommendations(db: Session, product_id: int, top_n: int = 5) -> List[models.Product]:
        """Recommendations based on a specific product (Similar items)"""
        product_ids = recommender.get_recommendations(db, product_id=product_id, top_n=top_n)
        return db.query(models.Product).filter(models.Product.id.in_(product_ids)).all()

    @staticmethod
    def get_personalized_recommendations(db: Session, user_id: int, top_n: int = 10) -> List[models.Product]:
        """Recommendations based on user profile and history"""
        product_ids = recommender.get_recommendations(db, user_id=user_id, top_n=top_n)
        return db.query(models.Product).filter(models.Product.id.in_(product_ids)).all()

    @staticmethod
    def get_trending_recommendations(db: Session, top_n: int = 5) -> List[models.Product]:
        """Popular items overall"""
        product_ids = recommender.get_recommendations(db, top_n=top_n)
        return db.query(models.Product).filter(models.Product.id.in_(product_ids)).all()

    @staticmethod
    def trigger_rebuild(db: Session):
        """Manually trigger model retraining"""
        recommender.fit(db)
        return {"status": "success", "message": "Model retraining initiated"}
