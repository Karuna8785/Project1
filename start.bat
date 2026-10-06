@echo off
title SmartERP - Enterprise Platform Launcher
cls
echo ===================================================
echo             SmartERP Enterprise Platform
echo  Modules: Auth, HR, Inventory, Sales, Procurement
echo ===================================================
echo.

REM Determine current directory
set "ROOT_DIR=%~dp0"

echo [1/2] Launching FastAPI Backend (Uvicorn)...
start "SmartERP Backend (FastAPI)" cmd /k "cd /d "%ROOT_DIR%backend" && (if exist ".venv\Scripts\activate.bat" (call .venv\Scripts\activate.bat) else (echo No venv found, using system Python)) && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

echo [2/2] Launching React Vite Frontend...
start "SmartERP Frontend (Vite)" cmd /k "cd /d "%ROOT_DIR%frontend" && npm run dev"

echo.
echo ===================================================
echo SmartERP servers are starting up in separate windows!
echo - Frontend Portal: http://localhost:5173
echo - Backend API:     http://localhost:8000
echo - Swagger Docs:    http://localhost:8000/docs
echo ===================================================
echo.
pause
