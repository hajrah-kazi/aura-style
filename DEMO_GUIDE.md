# 🚀 QUICK SETUP FOR DEMO (Presentation Day)

Follow these steps on the day of your presentation to make sure everything works perfectly for the demo.

---

## 1. Prerequisites
*   Make sure **Python 3.11+** is installed.
*   Make sure **Node.js 18+** is installed.
*   (Optional but Recommended) Have **Docker Desktop** running.

---

## 2. One-Click Startup (Recommended)
If you are on Windows, simply double-click:
`run_pro.bat`

This script will:
1.  Start the FastAPI Backend.
2.  Start the Next.js Frontend.
3.  Open the browser for you.

---

## 3. Manual Startup (If double-click fails)

### **Step A: Start Backend**
```bash
cd server
venv\Scripts\activate
# Make sure model is trained and data is seeded
python seed.py 
uvicorn app.main:app --reload
```

### **Step B: Start Frontend**
```bash
cd client-pro
npm run dev
```

---

## 4. The "Demo Flow" (How to Show It)

1.  **Open the Home Page:** Show the clean, modern layout.
2.  **Login:** Use a test account (e.g., `testuser` / `password123`).
3.  **Show Personality:** Point out the **"Matched for You"** section. Explain that it’s empty because you haven’t interacted much yet.
4.  **Perform Interaction:** 
    *   Click on 3 different "Running Shoes".
    *   "Add to Cart" one of them.
5.  **The Magic Refresh:** 
    *   Go back to the home page or refresh.
    *   Show how the **"Matched for You"** section now shows more shoes or sporting goods!
6.  **Similar Products:** 
    *   Open a product page.
    *   Scroll down to **"You Might Also Like"**.
    *   Explain that this uses **NLP (Sentence Transformers)** to find semantic matches.
7.  **Trending:** Show the **"Trending Now"** section and explain the velocity algorithm.
8.  **Responsive Design:** Right-click > Inspect > Toggle Device Toolbar to show it works on Mobile.

---

## 5. Troubleshooting (Emergency)
*   **"Backend Errors":** Just restart the backend terminal and run `python seed.py` again.
*   **"Recommendations not updating":** The cache might be too strong for a live demo. Change `CACHE_ENABLED=False` in your `.env` file for the demo.
*   **"Images not loading":** Make sure you have an active internet connection (the images usually come from Unsplash or a CDN).

---

**Good luck with your presentation!**
**AuraStyle is ready to impress.**
