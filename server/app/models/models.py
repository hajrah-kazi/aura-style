from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    preferences = Column(JSON, default={}) # Store user interests/categories
    created_at = Column(DateTime, default=datetime.utcnow)

    interactions = relationship("Interaction", back_populates="user")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    category = Column(String, index=True)
    price = Column(Float)
    image_url = Column(String)
    rating = Column(Float, default=0.0)
    stock_count = Column(Integer, default=100)
    brand = Column(String)
    tags = Column(String)  # Comma-separated tags
    metadata_json = Column(JSON, default={}) # Flexible extra attributes
    
    interactions = relationship("Interaction", back_populates="product")

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    interaction_type = Column(String) # 'view', 'click', 'cart', 'purchase', 'rate'
    value = Column(Float, default=1.0) # Weight of interaction
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="interactions")
    product = relationship("Product", back_populates="interactions")
