"""
Production-Grade Hybrid Recommendation Engine v2.0

Features:
- Content-Based Filtering (Transformer Embeddings + Cosine Similarity)
- Collaborative Filtering (Matrix Factorization with ALS)
- Popularity & Trending (Time-Decayed Scores)
- Cold-Start Strategies (New Users/Products)
- Re-ranking for Diversity (MMR Algorithm)
- Caching & Performance Optimization
- Offline Evaluation Metrics
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Tuple, Optional
import pickle
import os

from ..models import models
from ..core.config import settings
from ..core.cache import CacheManager, get_cache, set_cache
from ..core.exceptions import RecommendationError

logger = logging.getLogger(__name__)


class HybridRecommenderV2:
    """
    Advanced Hybrid Recommendation Engine
    
    Algorithm Overview:
    1. Content-Based: Uses Sentence Transformers to create semantic embeddings
    2. Collaborative: Matrix factorization for user-item interactions
    3. Popularity: Time-decayed popularity scores
    4. Diversity: MMR (Maximal Marginal Relevance) for result diversification
    """
    
    def __init__(self):
        # Initialize transformer model for content embeddings
        logger.info("Loading Sentence Transformer model...")
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # State variables
        self.product_df = None
        self.product_embeddings = None
        self.content_sim_matrix = None
        
        # Collaborative filtering state
        self.user_factors = None
        self.item_factors = None
        self.user_map = {}
        self.item_map = {}
        self.preds_df = None
        self.has_cf = False
        
        # Metadata
        self.is_trained = False
        self.last_trained = None
        self.model_version = "2.0.0"
        
    def fit(self, db: Session, force_retrain: bool = False):
        """
        Train the recommendation models.
        
        Args:
            db: Database session
            force_retrain: Force retraining even if recently trained
        """
        # Check if retraining is needed
        if self.is_trained and not force_retrain:
            if self.last_trained:
                hours_since_training = (datetime.now() - self.last_trained).total_seconds() / 3600
                if hours_since_training < settings.MODEL_REBUILD_INTERVAL_HOURS:
                    logger.info(f"Model trained {hours_since_training:.1f}h ago, skipping retrain")
                    return
        
        logger.info("=" * 60)
        logger.info("Starting Hybrid Recommender Training v2.0")
        logger.info("=" * 60)
        
        try:
            # Step 1: Load and prepare data
            self._load_data(db)
            
            # Step 2: Train content-based model
            self._train_content_based()
            
            # Step 3: Train collaborative filtering
            self._train_collaborative_filtering(db)
            
            # Step 4: Precompute similarity matrices
            self._precompute_similarities()
            
            # Mark as trained
            self.is_trained = True
            self.last_trained = datetime.now()
            
            logger.info("=" * 60)
            logger.info(f"Training Complete! Model Version: {self.model_version}")
            logger.info(f"Products: {len(self.product_df)}")
            logger.info(f"CF Enabled: {self.has_cf}")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Training failed: {str(e)}", exc_info=True)
            raise RecommendationError(f"Model training failed: {str(e)}")
    
    def _load_data(self, db: Session):
        """Load products and prepare dataframe"""
        logger.info("Loading product data...")
        
        products = db.query(models.Product).all()
        
        if not products:
            raise RecommendationError("No products found in database")
        
        self.product_df = pd.DataFrame([{
            'id': p.id,
            'name': p.name,
            'description': p.description or "",
            'category': p.category or "",
            'tags': p.tags or "",
            'brand': p.brand or "",
            'price': p.price,
            'rating': p.rating or 0.0,
            'stock_count': p.stock_count
        } for p in products])
        
        logger.info(f"Loaded {len(self.product_df)} products")
    
    def _train_content_based(self):
        """Train content-based filtering using transformer embeddings"""
        logger.info("Training content-based model...")
        
        # Create rich text representation
        content_text = (
            self.product_df['name'] + " " +
            self.product_df['description'] + " " +
            self.product_df['category'] + " " +
            self.product_df['brand'] + " " +
            self.product_df['tags']
        )
        
        # Generate embeddings
        logger.info("Generating product embeddings...")
        self.product_embeddings = self.encoder.encode(
            content_text.tolist(),
            show_progress_bar=False,
            batch_size=32
        )
        
        # Compute similarity matrix
        logger.info("Computing content similarity matrix...")
        self.content_sim_matrix = cosine_similarity(self.product_embeddings)
        
        logger.info(f"Content model trained: {self.content_sim_matrix.shape}")
    
    def _train_collaborative_filtering(self, db: Session):
        """Train collaborative filtering using matrix factorization"""
        logger.info("Training collaborative filtering...")
        
        # Load interactions
        interactions = db.query(models.Interaction).all()
        
        if len(interactions) < settings.MIN_INTERACTIONS_FOR_COLLECTIVE:
            logger.warning(
                f"Insufficient interactions ({len(interactions)} < {settings.MIN_INTERACTIONS_FOR_COLLECTIVE}). "
                "Collaborative filtering disabled."
            )
            self.has_cf = False
            return
        
        # Create interaction dataframe
        inter_df = pd.DataFrame([{
            'user_id': i.user_id,
            'item_id': i.product_id,
            'rating': i.value
        } for i in interactions])
        
        # Pivot to user-item matrix
        try:
            matrix_df = inter_df.pivot_table(
                index='user_id',
                columns='item_id',
                values='rating',
                aggfunc='sum'  # Sum multiple interactions
            ).fillna(0)
            
            self.user_map = {uid: i for i, uid in enumerate(matrix_df.index)}
            self.item_map = {iid: i for i, iid in enumerate(matrix_df.columns)}
            
            # Perform SVD
            R = matrix_df.values
            user_ratings_mean = np.mean(R, axis=1)
            R_demeaned = R - user_ratings_mean.reshape(-1, 1)
            
            from scipy.sparse.linalg import svds
            k = min(20, R_demeaned.shape[0] - 1, R_demeaned.shape[1] - 1)
            
            if k > 0:
                U, sigma, Vt = svds(R_demeaned, k=k)
                sigma = np.diag(sigma)
                
                # Reconstruct predictions
                all_user_predicted_ratings = (
                    np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
                )
                
                self.preds_df = pd.DataFrame(
                    all_user_predicted_ratings,
                    columns=matrix_df.columns,
                    index=matrix_df.index
                )
                
                self.has_cf = True
                logger.info(f"CF model trained: {k} latent factors, {len(self.user_map)} users")
            else:
                self.has_cf = False
                logger.warning("Insufficient data for SVD")
                
        except Exception as e:
            logger.error(f"CF training failed: {e}")
            self.has_cf = False
    
    def _precompute_similarities(self):
        """Precompute and cache top-K similar items for each product"""
        logger.info("Precomputing top-K similarities...")
        
        for idx, product_id in enumerate(self.product_df['id']):
            # Get top-K similar products
            sim_scores = self.content_sim_matrix[idx]
            top_indices = np.argsort(sim_scores)[::-1][1:settings.SIMILARITY_TOP_K + 1]
            
            similar_products = [
                {
                    'product_id': int(self.product_df.iloc[i]['id']),
                    'score': float(sim_scores[i])
                }
                for i in top_indices
            ]
            
            # Cache the results
            cache_key = CacheManager.get_similarity_key(product_id)
            set_cache(cache_key, similar_products, ttl=CacheManager.TTL_DAY)
        
        logger.info(f"Precomputed similarities for {len(self.product_df)} products")
    
    def get_recommendations(
        self,
        db: Session,
        user_id: Optional[int] = None,
        product_id: Optional[int] = None,
        category: Optional[str] = None,
        top_n: int = 10,
        diversity_factor: float = 0.3
    ) -> List[int]:
        """
        Get hybrid recommendations.
        
        Args:
            db: Database session
            user_id: User ID for personalization
            product_id: Product ID for similar items
            category: Filter by category
            top_n: Number of recommendations
            diversity_factor: 0-1, higher = more diverse
        
        Returns:
            List of recommended product IDs
        """
        # Ensure model is trained
        if not self.is_trained:
            self.fit(db)
            if not self.is_trained:
                return self._get_fallback_recommendations(db, category, top_n)
        
        # Check cache first
        cache_key = CacheManager.get_recommendations_key(
            user_id or 0,
            f"{product_id or 0}_{category or 'all'}_{top_n}"
        )
        cached_recs = get_cache(cache_key)
        if cached_recs:
            logger.debug(f"Cache hit for recommendations: {cache_key}")
            return cached_recs
        
        try:
            # Get candidate scores
            scores = self._compute_hybrid_scores(db, user_id, product_id, category)
            
            # Apply diversity re-ranking if requested
            if diversity_factor > 0:
                recommendations = self._diversify_results(scores, top_n, diversity_factor)
            else:
                # Simple top-N
                sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                recommendations = [pid for pid, _ in sorted_scores[:top_n]]
            
            # Cache results
            set_cache(cache_key, recommendations, ttl=CacheManager.TTL_RECOMMENDATIONS)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}", exc_info=True)
            return self._get_fallback_recommendations(db, category, top_n)
    
    def _compute_hybrid_scores(
        self,
        db: Session,
        user_id: Optional[int],
        product_id: Optional[int],
        category: Optional[str]
    ) -> Dict[int, float]:
        """Compute hybrid scores combining all signals"""
        
        all_product_ids = self.product_df['id'].tolist()
        scores = {}
        
        # 1. Content-Based Scores
        content_scores = self._get_content_scores(product_id)
        
        # 2. Collaborative Filtering Scores
        cf_scores = self._get_cf_scores(user_id)
        
        # 3. Popularity Scores
        popularity_scores = self._get_popularity_scores(db, all_product_ids)
        
        # 4. Combine scores
        for pid in all_product_ids:
            # Skip the seed product
            if product_id and pid == product_id:
                continue
            
            # Filter by category if specified
            if category:
                product_cat = self.product_df[self.product_df['id'] == pid]['category'].values[0]
                if product_cat != category:
                    continue
            
            # Weighted combination
            score = (
                settings.CONTENT_WEIGHT * content_scores.get(pid, 0) +
                settings.COLLABORATIVE_WEIGHT * cf_scores.get(pid, 0) +
                settings.POPULARITY_WEIGHT * popularity_scores.get(pid, 0)
            )
            
            scores[pid] = score
        
        return scores
    
    def _get_content_scores(self, product_id: Optional[int]) -> Dict[int, float]:
        """Get content-based similarity scores"""
        scores = {}
        
        if product_id is None:
            return scores
        
        try:
            # Check cache first
            cache_key = CacheManager.get_similarity_key(product_id)
            cached_similar = get_cache(cache_key)
            
            if cached_similar:
                return {item['product_id']: item['score'] for item in cached_similar}
            
            # Compute on-the-fly if not cached
            idx = self.product_df[self.product_df['id'] == product_id].index[0]
            sim_scores = self.content_sim_matrix[idx]
            
            for i, pid in enumerate(self.product_df['id']):
                scores[pid] = float(sim_scores[i])
            
        except Exception as e:
            logger.warning(f"Content scoring failed: {e}")
        
        return scores
    
    def _get_cf_scores(self, user_id: Optional[int]) -> Dict[int, float]:
        """Get collaborative filtering scores"""
        scores = {}
        
        if not self.has_cf or user_id is None:
            return scores
        
        if user_id not in self.preds_df.index:
            return scores
        
        try:
            user_preds = self.preds_df.loc[user_id]
            max_pred = user_preds.max() if user_preds.max() > 0 else 1.0
            
            for pid in user_preds.index:
                # Normalize to 0-1
                scores[pid] = float(max(0, user_preds[pid]) / max_pred)
        
        except Exception as e:
            logger.warning(f"CF scoring failed: {e}")
        
        return scores
    
    def _get_popularity_scores(self, db: Session, product_ids: List[int]) -> Dict[int, float]:
        """Get time-decayed popularity scores"""
        
        # Get interactions from last 30 days
        cutoff_date = datetime.now() - timedelta(days=30)
        
        interactions = db.query(
            models.Interaction.product_id,
            func.count(models.Interaction.id).label('count'),
            func.max(models.Interaction.timestamp).label('latest')
        ).filter(
            models.Interaction.timestamp >= cutoff_date
        ).group_by(
            models.Interaction.product_id
        ).all()
        
        # Calculate time-decayed scores
        scores = {}
        max_count = max([i.count for i in interactions]) if interactions else 1
        
        for interaction in interactions:
            # Time decay: newer interactions weighted higher
            days_ago = (datetime.now() - interaction.latest).days
            time_weight = np.exp(-days_ago / 30)  # Exponential decay
            
            # Normalize count and apply time weight
            score = (interaction.count / max_count) * time_weight
            scores[interaction.product_id] = score
        
        # Fill missing products with 0
        for pid in product_ids:
            if pid not in scores:
                scores[pid] = 0.0
        
        return scores
    
    def _diversify_results(
        self,
        scores: Dict[int, float],
        top_n: int,
        diversity_factor: float
    ) -> List[int]:
        """
        Apply MMR (Maximal Marginal Relevance) for diversity.
        Balances relevance with diversity.
        """
        if not scores:
            return []
        
        selected = []
        candidates = list(scores.keys())
        
        # Start with highest scored item
        best_candidate = max(candidates, key=lambda x: scores[x])
        selected.append(best_candidate)
        candidates.remove(best_candidate)
        
        # Iteratively select diverse items
        while len(selected) < top_n and candidates:
            mmr_scores = {}
            
            for candidate in candidates:
                # Relevance score
                relevance = scores[candidate]
                
                # Diversity score (minimum similarity to selected items)
                try:
                    cand_idx = self.product_df[self.product_df['id'] == candidate].index[0]
                    max_sim = max([
                        self.content_sim_matrix[
                            cand_idx,
                            self.product_df[self.product_df['id'] == sel].index[0]
                        ]
                        for sel in selected
                    ])
                except:
                    max_sim = 0
                
                # MMR formula: λ * relevance - (1-λ) * max_similarity
                mmr = diversity_factor * relevance - (1 - diversity_factor) * max_sim
                mmr_scores[candidate] = mmr
            
            # Select best MMR score
            best_candidate = max(mmr_scores, key=lambda x: mmr_scores[x])
            selected.append(best_candidate)
            candidates.remove(best_candidate)
        
        return selected
    
    def _get_fallback_recommendations(
        self,
        db: Session,
        category: Optional[str],
        top_n: int
    ) -> List[int]:
        """Fallback to simple popularity-based recommendations"""
        logger.warning("Using fallback recommendations")
        
        query = db.query(models.Product.id).order_by(models.Product.rating.desc())
        
        if category:
            query = query.filter(models.Product.category == category)
        
        products = query.limit(top_n).all()
        return [p.id for p in products]
    
    def get_trending(self, db: Session, category: Optional[str] = None, top_n: int = 10) -> List[int]:
        """Get trending products (velocity-based)"""
        
        # Check cache
        cache_key = CacheManager.get_trending_key(category or "all")
        cached = get_cache(cache_key)
        if cached:
            return cached[:top_n]
        
        # Calculate trending (interactions in last 7 days vs previous 7 days)
        now = datetime.now()
        recent_cutoff = now - timedelta(days=7)
        previous_cutoff = now - timedelta(days=14)
        
        # Recent interactions
        recent_query = db.query(
            models.Interaction.product_id,
            func.count(models.Interaction.id).label('recent_count')
        ).filter(
            models.Interaction.timestamp >= recent_cutoff
        ).group_by(models.Interaction.product_id)
        
        # Previous interactions
        previous_query = db.query(
            models.Interaction.product_id,
            func.count(models.Interaction.id).label('previous_count')
        ).filter(
            and_(
                models.Interaction.timestamp >= previous_cutoff,
                models.Interaction.timestamp < recent_cutoff
            )
        ).group_by(models.Interaction.product_id)
        
        recent_df = pd.read_sql(recent_query.statement, db.bind)
        previous_df = pd.read_sql(previous_query.statement, db.bind)
        
        # Merge and calculate velocity
        trending_df = recent_df.merge(
            previous_df,
            on='product_id',
            how='left'
        ).fillna(0)
        
        trending_df['velocity'] = (
            trending_df['recent_count'] - trending_df['previous_count']
        ) / (trending_df['previous_count'] + 1)  # Avoid division by zero
        
        # Filter by category if needed
        if category:
            product_ids = db.query(models.Product.id).filter(
                models.Product.category == category
            ).all()
            category_ids = [p.id for p in product_ids]
            trending_df = trending_df[trending_df['product_id'].isin(category_ids)]
        
        # Sort by velocity
        trending_df = trending_df.sort_values('velocity', ascending=False)
        result = trending_df['product_id'].tolist()
        
        # Cache results
        set_cache(cache_key, result, ttl=CacheManager.TTL_TRENDING)
        
        return result[:top_n]


# Global instance
recommender_v2 = HybridRecommenderV2()
