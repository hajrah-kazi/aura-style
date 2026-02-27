"""
Redis caching utilities for high-performance data access.
"""
import json
import logging
from typing import Any, Optional, Callable
from functools import wraps
import hashlib

logger = logging.getLogger(__name__)

# Redis client will be initialized in main.py
redis_client = None


def init_redis(redis_url: str = None):
    """Initialize Redis connection"""
    global redis_client
    
    if not redis_url:
        logger.warning("Redis URL not provided, caching disabled")
        return None
    
    try:
        import redis
        redis_client = redis.from_url(redis_url, decode_responses=True)
        redis_client.ping()
        logger.info("Redis connection established")
        return redis_client
    except ImportError:
        logger.warning("Redis package not installed, caching disabled")
        return None
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return None


def get_cache(key: str) -> Optional[Any]:
    """Get value from cache"""
    if not redis_client:
        return None
    
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        logger.error(f"Cache get error for key {key}: {e}")
        return None


def set_cache(key: str, value: Any, ttl: int = 300) -> bool:
    """Set value in cache with TTL (default 5 minutes)"""
    if not redis_client:
        return False
    
    try:
        redis_client.setex(key, ttl, json.dumps(value))
        return True
    except Exception as e:
        logger.error(f"Cache set error for key {key}: {e}")
        return False


def delete_cache(key: str) -> bool:
    """Delete value from cache"""
    if not redis_client:
        return False
    
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        logger.error(f"Cache delete error for key {key}: {e}")
        return False


def clear_pattern(pattern: str) -> int:
    """Clear all keys matching pattern"""
    if not redis_client:
        return 0
    
    try:
        keys = redis_client.keys(pattern)
        if keys:
            return redis_client.delete(*keys)
        return 0
    except Exception as e:
        logger.error(f"Cache clear error for pattern {pattern}: {e}")
        return 0


def cache_key(*args, **kwargs) -> str:
    """Generate cache key from arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    key_string = ":".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()


def cached(ttl: int = 300, key_prefix: str = ""):
    """
    Decorator for caching function results.
    
    Usage:
        @cached(ttl=600, key_prefix="recommendations")
        def get_recommendations(user_id: int):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{key_prefix}:{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_value = get_cache(key)
            if cached_value is not None:
                logger.debug(f"Cache hit for {key}")
                return cached_value
            
            # Execute function
            logger.debug(f"Cache miss for {key}")
            result = await func(*args, **kwargs)
            
            # Store in cache
            set_cache(key, result, ttl)
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{key_prefix}:{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_value = get_cache(key)
            if cached_value is not None:
                logger.debug(f"Cache hit for {key}")
                return cached_value
            
            # Execute function
            logger.debug(f"Cache miss for {key}")
            result = func(*args, **kwargs)
            
            # Store in cache
            set_cache(key, result, ttl)
            
            return result
        
        # Return appropriate wrapper based on function type
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator


class CacheManager:
    """Centralized cache management"""
    
    # Cache TTLs (in seconds)
    TTL_SHORT = 60          # 1 minute
    TTL_MEDIUM = 300        # 5 minutes
    TTL_LONG = 900          # 15 minutes
    TTL_VERY_LONG = 3600    # 1 hour
    TTL_DAY = 86400         # 24 hours
    
    # Cache key prefixes
    PREFIX_RECOMMENDATIONS = "rec"
    PREFIX_TRENDING = "trending"
    PREFIX_PRODUCT = "product"
    PREFIX_USER = "user"
    PREFIX_SIMILARITY = "similarity"
    
    @staticmethod
    def get_recommendations_key(user_id: int, context: str = "default") -> str:
        """Generate cache key for user recommendations"""
        return f"{CacheManager.PREFIX_RECOMMENDATIONS}:{user_id}:{context}"
    
    @staticmethod
    def get_trending_key(category: str = "all") -> str:
        """Generate cache key for trending products"""
        return f"{CacheManager.PREFIX_TRENDING}:{category}"
    
    @staticmethod
    def get_product_key(product_id: int) -> str:
        """Generate cache key for product data"""
        return f"{CacheManager.PREFIX_PRODUCT}:{product_id}"
    
    @staticmethod
    def get_similarity_key(product_id: int) -> str:
        """Generate cache key for product similarity"""
        return f"{CacheManager.PREFIX_SIMILARITY}:{product_id}"
    
    @staticmethod
    def invalidate_user_cache(user_id: int):
        """Invalidate all cache for a user"""
        pattern = f"{CacheManager.PREFIX_RECOMMENDATIONS}:{user_id}:*"
        return clear_pattern(pattern)
    
    @staticmethod
    def invalidate_product_cache(product_id: int):
        """Invalidate all cache for a product"""
        patterns = [
            f"{CacheManager.PREFIX_PRODUCT}:{product_id}",
            f"{CacheManager.PREFIX_SIMILARITY}:{product_id}"
        ]
        count = 0
        for pattern in patterns:
            count += clear_pattern(pattern)
        return count
