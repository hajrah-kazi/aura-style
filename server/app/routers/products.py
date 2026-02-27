from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..models import models
from ..schemas.schemas import ProductOut, ProductCreate, InteractionCreate
from .auth import get_current_user_optional

router = APIRouter()

@router.get("/", response_model=List[ProductOut])
def list_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)
    if category:
        query = query.filter(models.Product.category == category)
    if search:
        query = query.filter(models.Product.name.contains(search) | models.Product.description.contains(search))
    return query.all()

@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int, 
    db: Session = Depends(get_db),
    user: Optional[models.User] = Depends(get_current_user_optional)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Track interaction if user is logged in
    if user:
        interaction = models.Interaction(
            user_id=user.id,
            product_id=product_id,
            interaction_type="view",
            value=1.0
        )
        db.add(interaction)
        db.commit()
        
    return product

@router.post("/{product_id}/interact")
def interact_with_product(
    product_id: int,
    interaction_data: InteractionCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user_optional)
):
    if not user:
        return {"status": "ignored", "reason": "not_authenticated"}
        
    interaction = models.Interaction(
        user_id=user.id,
        product_id=product_id,
        interaction_type=interaction_data.interaction_type,
        value=interaction_data.value
    )
    db.add(interaction)
    db.commit()
    return {"status": "success"}

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
