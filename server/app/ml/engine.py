import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from sqlalchemy import func
import os
import logging
from ..models import models
from ..core.config import settings

logger = logging.getLogger(__name__)

class HybridRecommender:
    def __init__(self):
        # Initialize models
        # Using a very lightweight transformer for embeddings
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Collaborative filtering state (Manual Matrix Factorization)
        self.user_factors = None
        self.item_factors = None
        self.user_map = {}
        self.item_map = {}
        
        # Content state
        self.product_df = None
        self.content_sim_matrix = None
        self.is_trained = False

    def fit(self, db: Session):
        """
        Trains both content-based and collaborative filtering models.
        """
        logger.info("Starting model training...")
        
        # 1. Load Data
        products = db.query(models.Product).all()
        interactions = db.query(models.Interaction).all()
        
        if not products:
            logger.warning("No products found to train on.")
            return

        self.product_df = pd.DataFrame([{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'category': p.category,
            'tags': p.tags or ""
        } for p in products])

        # 2. Content-Based: Transformer Embeddings
        logger.info("Computing product embeddings...")
        content_text = self.product_df['name'] + " " + \
                       self.product_df['description'] + " " + \
                       self.product_df['category'] + " " + \
                       self.product_df['tags']
        
        embeddings = self.encoder.encode(content_text.tolist(), show_progress_bar=False)
        self.content_sim_matrix = cosine_similarity(embeddings)
        
        # 3. Collaborative Filtering: Simple Matrix Factorization (SVD via NumPy)
        if len(interactions) >= settings.MIN_INTERACTIONS_FOR_COLLECTIVE:
            logger.info("Training Collaborative Filtering (Manual SVD)...")
            inter_df = pd.DataFrame([{
                'user_id': i.user_id,
                'item_id': i.product_id,
                'rating': i.value
            } for i in interactions])
            
            # Pivot to matrix (using pivot_table to handle duplicates)
            matrix_df = inter_df.pivot_table(index='user_id', columns='item_id', values='rating', aggfunc='mean').fillna(0)
            self.user_map = {uid: i for i, uid in enumerate(matrix_df.index)}
            self.item_map = {iid: i for i, iid in enumerate(matrix_df.columns)}
            
            R = matrix_df.values
            user_ratings_mean = np.mean(R, axis=1)
            R_demeaned = R - user_ratings_mean.reshape(-1, 1)
            
            # Singular Value Decomposition
            from scipy.sparse.linalg import svds
            k = min(10, R_demeaned.shape[0]-1, R_demeaned.shape[1]-1)
            if k > 0:
                U, sigma, Vt = svds(R_demeaned, k=k)
                sigma = np.diag(sigma)
                
                # Reconstruct predicted ratings
                all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
                self.preds_df = pd.DataFrame(all_user_predicted_ratings, columns=matrix_df.columns, index=matrix_df.index)
                self.has_cf = True
            else:
                self.has_cf = False
        else:
            logger.warning("Insufficient interaction data for Collaborative Filtering.")
            self.has_cf = False

        self.is_trained = True
        logger.info("Model training complete.")

    def get_recommendations(self, db: Session, user_id: int = None, product_id: int = None, top_n: int = 10):
        if not self.is_trained:
            self.fit(db)
            if not self.is_trained: return []

        all_product_ids = self.product_df['id'].tolist()
        
        # 1. Content-Based Scores
        content_scores = np.zeros(len(all_product_ids))
        if product_id is not None:
            try:
                idx = self.product_df[self.product_df['id'] == product_id].index[0]
                content_scores = self.content_sim_matrix[idx]
            except: pass

        # 2. Collaborative Filtering Scores
        cf_scores = np.zeros(len(all_product_ids))
        if user_id is not None and self.has_cf and user_id in self.preds_df.index:
            user_preds = self.preds_df.loc[user_id]
            for i, pid in enumerate(all_product_ids):
                if pid in user_preds.index:
                    cf_scores[i] = user_preds[pid] / 5.0 # Normalize

        # 3. Popularity Scores
        popularity_scores = self._get_popularity_scores(db, all_product_ids)

        # 4. Hybrid Logic
        final_scores = []
        for i, pid in enumerate(all_product_ids):
            if product_id and pid == product_id: continue
            
            score = (
                settings.CONTENT_WEIGHT * content_scores[i] +
                settings.COLLABORATIVE_WEIGHT * cf_scores[i] +
                settings.POPULARITY_WEIGHT * popularity_scores.get(pid, 0)
            )
            final_scores.append((pid, score))

        final_scores.sort(key=lambda x: x[1], reverse=True)
        return [x[0] for x in final_scores[:top_n]]

    def _get_popularity_scores(self, db: Session, product_ids):
        interactions = db.query(
            models.Interaction.product_id, 
            func.count(models.Interaction.id).label('count')
        ).group_by(models.Interaction.product_id).all()
        
        counts = {i.product_id: i.count for i in interactions}
        max_count = max(counts.values()) if counts else 1
        return {pid: (counts.get(pid, 0) / max_count) for pid in product_ids}

recommender = HybridRecommender()
