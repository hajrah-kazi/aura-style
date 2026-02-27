from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None
    preferences: Optional[dict] = None

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: str
    category: str
    price: float
    image_url: Optional[str] = None
    tags: Optional[str] = None
    brand: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    rating: float
    stock_count: int
    metadata_json: Optional[dict] = None
    
    class Config:
        from_attributes = True

# Interaction Schemas
class InteractionCreate(BaseModel):
    product_id: int
    interaction_type: str # 'view', 'click', 'cart', 'purchase'
    value: Optional[float] = 1.0

class InteractionOut(InteractionCreate):
    id: int
    user_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
