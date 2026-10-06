@echo off
echo ========================================================
echo Starting SmartERP (FastAPI Backend + Vite/React Frontend)
echo ========================================================

:: 1. Launch FastAPI Backend in a new window
echo Starting FastAPI Backend on http://localhost:8000 ...
start "SmartERP Backend" powershell -NoExit -Command "cd backend; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

:: 2. Launch Vite Frontend in a new window
echo Starting React Vite Frontend on http://localhost:5173 ...
start "SmartERP Frontend" powershell -NoExit -Command "cd frontend; npm run dev"

echo.
echo ========================================================
echo SmartERP services are starting!
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo Swagger:  http://localhost:8000/docs
echo ========================================================
