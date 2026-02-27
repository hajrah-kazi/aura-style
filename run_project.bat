@echo off
echo Starting Backend...
start "Backend Server" cmd /k "server\run.bat"

echo Starting Frontend...
start "Frontend Client" cmd /k "cd client && npm run dev"

echo All services started!
echo Frontend: http://localhost:5173
echo Backend: http://localhost:8000
pause
