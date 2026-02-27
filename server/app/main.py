from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .core.config import settings
from .core.database import engine, Base
from sqlalchemy import text
from .core.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)
from .core.middleware import (
    RequestLoggingMiddleware,
    RateLimitMiddleware,
    SecurityHeadersMiddleware
)
from .core.cache import init_redis
from .routers import auth, products, recommendations
import logging
from datetime import datetime
from fastapi import HTTPException

# Setup Enhanced Logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Database Tables
logger.info("Initializing database...")
Base.metadata.create_all(bind=engine)

# Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-grade e-commerce platform with hybrid ML recommendation engine",
    docs_url="/docs" if settings.DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None
)

# Initialize Redis Cache
if settings.REDIS_URL:
    logger.info("Initializing Redis cache...")
    init_redis(settings.REDIS_URL)
else:
    logger.warning("Redis not configured - caching disabled")

# Register Exception Handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Add Middleware (order matters - last added runs first)
app.add_middleware(SecurityHeadersMiddleware)

if settings.RATE_LIMIT_ENABLED:
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=settings.RATE_LIMIT_PER_MINUTE
    )

app.add_middleware(RequestLoggingMiddleware)

# CORS Configuration (Production-Ready)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.ENVIRONMENT == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    expose_headers=["X-Correlation-ID", "X-Process-Time"]
)

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api/products", tags=["Catalog"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["ML Recommendations"])

# Health Check Endpoints
@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "environment": settings.ENVIRONMENT,
        "documentation": "/docs" if settings.DEBUG else "disabled"
    }


@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    Returns detailed system health status.
    """
    from .core.database import SessionLocal
    from .core.cache import redis_client
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "checks": {}
    }
    
    # Check Database
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["checks"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check Redis Cache
    if redis_client:
        try:
            redis_client.ping()
            health_status["checks"]["cache"] = "healthy"
        except Exception as e:
            health_status["checks"]["cache"] = f"unhealthy: {str(e)}"
            health_status["status"] = "degraded"
    else:
        health_status["checks"]["cache"] = "disabled"
    
    # Check ML Engine
    try:
        from .ml.engine import recommender
        health_status["checks"]["ml_engine"] = "loaded" if recommender.is_trained else "not_trained"
    except Exception as e:
        health_status["checks"]["ml_engine"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
    
    return health_status


@app.get("/metrics", tags=["System"])
async def metrics():
    """
    Basic metrics endpoint for monitoring.
    In production, use Prometheus or similar.
    """
    from .core.database import SessionLocal
    from .models import models
    
    db = SessionLocal()
    try:
        metrics_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "counts": {
                "users": db.query(models.User).count(),
                "products": db.query(models.Product).count(),
                "interactions": db.query(models.Interaction).count()
            }
        }
        return metrics_data
    finally:
        db.close()


# Startup Event
@app.on_event("startup")
async def startup_event():
    """Run tasks on application startup"""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Cache enabled: {settings.CACHE_ENABLED}")
    logger.info(f"Rate limiting: {settings.RATE_LIMIT_ENABLED}")


# Shutdown Event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info("Shutting down application...")
    # Close Redis connection if exists
    from .core.cache import redis_client
    if redis_client:
        redis_client.close()
        logger.info("Redis connection closed")
