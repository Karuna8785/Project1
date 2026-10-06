@echo off
echo ========================================
echo  SmartERP - Member 2: HR Management
echo ========================================
echo.

echo [1/2] Starting FastAPI backend...
start "SmartERP Backend" powershell -NoExit -Command ^
  "cd '%~dp0backend'; if (-not (Test-Path .venv)) { python -m venv .venv }; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt -q; uvicorn app.main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting React frontend...
start "SmartERP Frontend" powershell -NoExit -Command ^
  "cd '%~dp0frontend'; npm install; npm run dev"

echo.
echo ========================================
echo  Backend:  http://localhost:8000
echo  Frontend: http://localhost:5173
echo  Swagger:  http://localhost:8000/docs
echo ========================================
pause
