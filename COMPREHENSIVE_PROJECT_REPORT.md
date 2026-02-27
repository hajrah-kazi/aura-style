# AuraStyle: Comprehensive Project Documentation

## 1. Project Overview

**Project Name**: AuraStyle (Microproject)
**Description**: 
AuraStyle is a production-grade, enterprise-level e-commerce platform featuring an advanced **Hybrid Recommendation Engine**. It is designed to provide highly personalized shopping experiences by leveraging state-of-the-art machine learning techniques, including Content-Based Filtering with Transformer models (NLP) and Collaborative Filtering with Matrix Factorization (SVD). 

The platform is engineered for high performance, scalability, and security, utilizing a modern tech stack with React/Next.js on the frontend and FastAPI/Python on the backend, fully containerized with Docker.

---

## 2. Technology Stack

### 2.1 Backend (Server)
*   **Framework**: **FastAPI** (Python 3.11+) - chosen for its high performance (async/await) and automatic API documentation (Swagger UI).
*   **ORM**: **SQLAlchemy** - for database interactions and ORM.
*   **Authentication**: **JWT (JSON Web Tokens)** via `python-jose` and `passlib` for secure, stateless authentication and bcrypt password hashing.
*   **Data Validation**: **Pydantic** - for strict data validation and serialization.
*   **Server**: **Uvicorn** (ASGI server) and **Gunicorn** (Production process manager).
*   **Database**: **SQLite** (Development) / **PostgreSQL** (Production-ready).

### 2.2 Frontend (Client-Pro)
*   **Framework**: **Next.js 14** (App Router) - for server-side rendering, routing, and optimization.
*   **Library**: **React 18** - for building component-based user interfaces.
*   **Language**: **TypeScript** - for type safety and better developer experience.
*   **Styling**: **Tailwind CSS** - for utility-first, responsive design.
*   **Animations**: **Framer Motion** - for advanced UI transitions and animations.
*   **State Management**: **Zustand** - for lightweight global state management.
*   **HTTP Client**: **Axios** - for making API requests.
*   **Icons**: **Lucide React** - for consistent and scalable iconography.

### 2.3 Machine Learning & Data Science
*   **NLP / Embeddings**: **Sentence Transformers (`all-MiniLM-L6-v2`)** - to generate 384-dimensional semantic embeddings for product data.
*   **Collaborative Filtering**: **Scikit-learn / SciPy** - specifically **Truncated SVD (Singular Value Decomposition)** for matrix factorization.
*   **Data Processing**: **Pandas** and **NumPy** - for efficient data manipulation and numerical operations.
*   **Similarity Search**: **Cosine Similarity** (via scikit-learn).

### 2.4 Infrastructure & DevOps
*   **Containerization**: **Docker** & **Docker Compose** - for consistent environments and easy deployment.
*   **Caching**: **Redis** - for high-performance caching of recommendations, similarity matrices, and rate limiting.
*   **Version Control**: Git.

---

## 3. Core Logic & Algorithms

### 3.1 Hybrid Recommendation Engine
The core of AuraStyle is its `HybridRecommenderV2` class, which combines three distinct recommendation strategies to maximize relevance and coverage.

#### A. Content-Based Filtering (NLP)
*   **Logic**: Recommends items similar to those a user has liked based on product metadata.
*   **Algorithm**: 
    1.  Concatenates product fields: `Name + Description + Category + Brand + Tags`.
    2.  Uses **SentenceTransformer ('all-MiniLM-L6-v2')** to encode this text into **384-dimensional dense vectors (embeddings)**.
    3.  Computes **Cosine Similarity** between all product vectors to create a similarity matrix.
    4.  **Advantage**: Solves the "Cold Start" problem for new items (they can be recommended as soon as metadata is available).

#### B. Collaborative Filtering (CF)
*   **Logic**: Recommends items based on the behavior of similar users. "Users who liked X also liked Y."
*   **Algorithm**:
    1.  Constructs a **User-Item Interaction Matrix** where rows are users, columns are products, and values are interaction strengths (e.g., View=1, Cart=3, Purchase=5).
    2.  Applies **Singular Value Decomposition (SVD)** from `scipy.sparse.linalg.svds`.
    3.  Decomposes the matrix into three lower-rank matrices ($U, \Sigma, V^T$) to discover latent factors (hidden patterns) connecting users and items.
    4.  Reconstructs the matrix to predict missing scores (potential interest) for items a user hasn't seen yet.
    5.  **Advantage**: Captures complex user behavior patterns that content analysis might miss.

#### C. Popularity & Trending
*   **Logic**: Recommends items that are currently popular or trending upwards.
*   **Algorithm**:
    1.  **Exponential Time Decay**: Interactions are weighted by recency. Older interactions have less influence.
    2.  **Formula**: $Score = \frac{Count}{MaxCount} \times e^{(-\frac{DaysAgo}{30})}$.
    3.  **Velocity**: Calculates the change in interaction volume over the last 7 days vs. the previous 7 days to identify "rising stars".

#### D. Hybrid Scoring & Diversity
*   **Final Scoring Formula**: The system combines the scores from the above methods using configurable weights:
    $$Final Score = (0.35 \times ContentScore) + (0.40 \times CFScore) + (0.15 \times PopularityScore)$$
*   **Diversity Re-ranking (MMR)**:
    *   To avoid "filter bubbles" (showing only very similar items), the system uses **Maximal Marginal Relevance (MMR)**.
    *   It re-ranks the top candidates to balance **Relevance** (high score) with **Diversity** (dissimilarity to already selected items).

### 3.2 Key Features & Capabilities

#### User Experience (UX) features
1.  **Personalized Feed**: A unique "Matched for You" section on the homepage tailored to the user's history.
2.  **Trending Products**: Real-time display of products gaining popularity.
3.  **Similar Products**: "You might also like" section on product detail pages (Contextual recommendations).
4.  **Smart Search**: Semantic search capabilities (future roadmap enabled by embeddings).

#### Security Features
1.  **Rate Limiting**: Custom middleware limits requests (default: 60/min) per IP address to prevent abuse/DDoS.
2.  **Stateless Auth**: Full JWT implementation means the server doesn't need to store session data, improving scalability.
3.  **Security Headers**: Automated injection of security headers (XSS-Protection, Content-Security-Policy, etc.).
4.  **Request Tracing**: Every request is assigned a `Correlation-ID` for end-to-end debugging and logging.

#### Performance Features
1.  **Redis Caching**: 
    *   **Similarity Matrix**: Top-K similar items are precomputed and cached.
    *   **API Responses**: Expensive recommendation queries are cached for 5 minutes.
2.  **Optimized Database Queries**: usage of SQLAlchemy with eager loading to prevent N+1 query problems.

---

## 4. Project Structure

### 4.1 Backend (`/server`)
*   `app/main.py`: Application entry point, app configuration.
*   `app/core/`: 
    *   `config.py`: Environment variable management.
    *   `middleware.py`: Security and logging middleware.
    *   `cache.py`: Redis cache manager wrapper.
*   `app/models/`: SQLAlchemy database models (`User`, `Product`, `Interaction`).
*   `app/schemas/`: Pydantic data schemas for request/response validation.
*   `app/routers/`: API route handlers (`auth`, `products`, `recommendations`).
*   `app/ml/`: 
    *   `engine_v2.py`: The Hybrid Recommendation Engine logic.
*   `seed.py`: Script to populate the database with initial dummy data.

### 4.2 Frontend (`/client-pro`)
*   `app/`: Next.js App Router pages.
    *   `page.tsx`: Home page (Feed).
    *   `(auth)/`: Login and Register pages.
    *   `catalog/`: Product listing.
    *   `product/[id]/`: Product detail view.
*   `components/`: Reusable React components (`Navbar`, `ProductCard`, `Button`, etc.).
*   `lib/`: 
    *   `api.ts`: API client configurations.
    *   `store.ts`: Zustand global state store.
*   `tailwind.config.ts`: Design system configuration (colors, fonts, animations).

---

## 5. Summary

The **AuraStyle** project represents a significant leap from a basic e-commerce site to a sophisticated, intelligent platform. By integrating a commercial-grade **Hybrid Recommendation Engine**, it moves beyond simple database queries to offer predictive, personalized experiences akin to Netflix or Amazon. 

The architecture is built for **real-world deployment**, prioritizing not just the "happy path" but also reliability (caching, error handling), security (rate limiting, strict auth), and maintainability (clean code, modular design). This project demonstrates proficiency in Full Stack Development, Machine Learning Engineering, and DevOps principles.
