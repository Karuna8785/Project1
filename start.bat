@echo off
title SmartERP Launcher - Procurement & Finance
cls
echo ===============================================================================
echo                     SMARTERP ENTERPRISE PLATFORM
echo          Procurement & Finance Management (Suppliers, POs, Expenses, AP)
echo ===============================================================================
echo.
echo [1/3] Checking environment...

cd /d "%~dp0"

if not exist "backend\.venv\Scripts\python.exe" (
    echo [ERROR] Python virtual environment not found in backend\.venv
    echo Please create it using: cd backend ^& python -m venv .venv ^& .\.venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo [ERROR] Frontend node_modules not found.
    echo Please run: cd frontend ^& npm install
    pause
    exit /b 1
)

echo [2/3] Launching FastAPI Backend on http://localhost:8000 ...
start "SmartERP Backend (FastAPI)" powershell -NoExit -Command "cd '%~dp0backend'; .\.venv\Scripts\activate; uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [3/3] Launching React Vite Frontend on http://localhost:5173 ...
start "SmartERP Frontend (Vite)" powershell -NoExit -Command "cd '%~dp0frontend'; npm.cmd run dev"

echo.
echo ===============================================================================
echo SmartERP services are starting up!
echo.
echo   - Frontend Portal:    http://localhost:5173
echo   - Backend API:        http://localhost:8000
echo   - Swagger API Docs:   http://localhost:8000/docs
echo   - ReDoc API Docs:     http://localhost:8000/redoc
echo.
echo Pre-configured Test Accounts:
echo   - Admin User:         admin / Admin@123
echo   - Procurement Lead:   sarah.procure / Procure@123
echo   - Finance Controller: david.finance / Finance@123
echo ===============================================================================
echo.
pause
