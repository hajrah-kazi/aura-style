@echo off
echo ==========================================
echo    AuraStyle ML ^| Intelligent Store
echo ==========================================

echo [1/3] Refreshing Data...
cd server
set PYTHONPATH=.
venv-pro\Scripts\python seed.py
cd ..

echo [2/3] Starting Backend Server...
start "AuraStyle Backend" cmd /k "cd server && set PYTHONPATH=. && venv-pro\Scripts\python -m uvicorn app.main:app --reload"

echo [3/3] Starting Modern Frontend...
start "AuraStyle Frontend" cmd /k "cd client-pro && npm install && npm run dev"

echo ==========================================
echo SERVICES RUNNING:
echo - API: http://localhost:8000/docs
echo - UI:  http://localhost:3000
echo ==========================================
pause
