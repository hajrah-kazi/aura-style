# 💻 TECHNICAL EXPLAINER: How the Code Works

This document is your "Cheat Sheet" for explaining the code to an examiner or colleague.

---

## 1. Backend: The Engine (FastAPI & ML)

### **A. Recommendation Logic (`server/app/ml/engine_v2.py`)**
This is the heart of the project.
*   **The `fit()` method:** This is where the model "learns". It loads product data and user interactions from the database, generates embeddings for content, and calculates the SVD for collaborative filtering.
*   **Content-Based (`_train_content_based()`):**
    *   We use **Sentence Transformers** (`all-MiniLM-L6-v2`).
    *   It takes name, description, and brand, and turns them into a 384-element list of numbers (embeddings).
    *   We then calculate **Cosine Similarity** between these lists. If the angle between two vectors is small (close to 1), the products are semantically similar.
*   **Collaborative Filtering (`_train_collaborative_filtering()`):**
    *   We build a **User-Item Matrix**.
    *   We use **SVD (Singular Value Decomposition)** to handle "sparsity" (where users haven't seen most products).
    *   It predicts a score for every product for every user based on "Latent Factors" (hidden patterns).
*   **Hybrid Scoring (`_compute_hybrid_scores()`):**
    *   It takes scores from Content, CF, and Popularity.
    *   It applies weights (35%, 40%, 15%) to get the final score.
*   **Diversity (`_diversify_results()`):**
    *   Uses **MMR (Maximal Marginal Relevance)**. It makes sure that if you see one red shirt, the rest of the list isn't *only* red shirts, even if they have high scores.

### **B. Main Application (`server/app/main.py`)**
*   **FastAPI:** Chosen for its `async` capabilities, which means it can handle many users at once without slowing down.
*   **Middleware:** We have three custom middlewares:
    1.  **Logging:** Records every request for debugging.
    2.  **Rate Limiting:** Prevents a single user from crashing the site by sending too many requests (60 per minute).
    3.  **Security Headers:** Adds standard protection like XSS and CSP.
*   **Validation:** Uses **Pydantic** models to ensure that the data sent to the API is in the correct format (e.g., price must be a number).

---

## 2. Frontend: The Interface (Next.js & Tailwind)

### **A. App Router (`client-pro/app/`)**
*   **Next.js 14:** Uses the latest "App Router" for server-side rendering, which makes the site load faster and helps with SEO.
*   **Client vs Server Components:** Heavy components (like the Recommendation Feed) are rendered on the server to reduce the work for the user's phone or computer.

### **B. Animations (`Framer Motion`)**
*   We use **Framer Motion** for "Micro-animations". When you hover over a product, it subtly scales or glows. This makes the site feel "Premium" and desktop-app-like.

### **C. State Management (`Zustand`)**
*   **Zustand** is used to store things like the shopping cart or user login state. It's much faster and easier to use than Redux.

---

## 3. Infrastructure: Docker & Redis

### **A. Docker (`docker-compose.yml`)**
*   Docker packages the app into "containers".
*   This ensures that the project runs exactly the same on your computer as it would on a real server.
*   One command (`docker-compose up`) starts the Flask backend, the React frontend, the PostgreSQL database, and the Redis cache all at once.

### **B. Redis Cache**
*   Why? Training an ML model is slow.
*   We store the results in **Redis** (an in-memory database).
*   When a user refreshes the page, the server gets the data from Redis in <5ms instead of 500ms.

---

## 4. Database Schema (SQLAlchemy)
*   **Models (`server/app/models/models.py`):**
    *   `User`: Hashed password (never store plain passwords!).
    *   `Product`: Category, Price, Tags.
    *   `Interaction`: Links User + Product + Weight (View=1, Purchase=5).

---

## 💡 How to answer "What did YOU do?"
*   "I built a production-grade e-commerce backend using **FastAPI**."
*   "I implemented a **hybrid recommendation system** that combines Natural Language Processing for content and SVD for user behavior."
*   "I optimized the system using **Redis** for caching and **MMR** for diversity."
*   "I ensured the app is secure with **JWT authentication** and **Rate Limiting**."
*   "I created a high-end frontend with **Next.js 14** and **Tailwind CSS** for a premium user experience."
