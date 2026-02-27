import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "AuraStyle - Intelligent E-Commerce Platform"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY_FOR_JWT_123456789_CHANGE_IN_PRODUCTION")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # CORS - Environment-based
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    
    # Redis Cache
    REDIS_URL: str = os.getenv("REDIS_URL", "")  # Empty string = caching disabled
    CACHE_ENABLED: bool = bool(os.getenv("REDIS_URL", ""))
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # ML Settings
    MODEL_REBUILD_INTERVAL_HOURS: int = 24
    MIN_INTERACTIONS_FOR_COLLECTIVE: int = 10
    SIMILARITY_TOP_K: int = 50  # Number of similar items to precompute
    
    # Recommendation Weights (Hybrid Algorithm)
    CONTENT_WEIGHT: float = 0.35
    COLLABORATIVE_WEIGHT: float = 0.40
    POPULARITY_WEIGHT: float = 0.15
    DIVERSITY_WEIGHT: float = 0.10
    
    # Cold Start Settings
    COLD_START_MIN_INTERACTIONS: int = 3
    NEW_USER_BOOST_DAYS: int = 7
    NEW_PRODUCT_BOOST_DAYS: int = 14
    
    # Cache TTLs (seconds)
    CACHE_TTL_RECOMMENDATIONS: int = 300      # 5 minutes
    CACHE_TTL_TRENDING: int = 900             # 15 minutes
    CACHE_TTL_PRODUCT: int = 3600             # 1 hour
    CACHE_TTL_SIMILARITY: int = 86400         # 24 hours
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
