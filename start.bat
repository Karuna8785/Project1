@echo off
echo ===================================================
echo             SmartERP - Starting System
echo  Member 1: Authentication & Security
echo  Member 5: Sales Management System (Active)
echo ===================================================
echo.

REM Determine current directory
set "ROOT_DIR=%~dp0"

echo [1/2] Launching FastAPI Backend (Uvicorn)...
start "SmartERP Backend (FastAPI)" powershell -NoExit -Command "cd '%ROOT_DIR%backend'; if (Test-Path .venv\Scripts\activate) { .\.venv\Scripts\activate }; uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

echo [2/2] Launching React Vite Frontend...
start "SmartERP Frontend (Vite)" powershell -NoExit -Command "cd '%ROOT_DIR%frontend'; npm run dev"

echo.
echo ===================================================
echo SmartERP servers are starting up in separate windows!
echo - Frontend:    http://localhost:5173
echo - Backend API: http://localhost:8000
echo - Swagger Docs: http://localhost:8000/docs
echo ===================================================
echo.
pause
