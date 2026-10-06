@echo off
TITLE SmartERP Launcher
echo ============================================================================
echo                      Starting SmartERP Platform
echo ============================================================================
echo.

SET ROOT_DIR=%~dp0
cd /d "%ROOT_DIR%"

:: Check if Node is in PATH, if not fallback to portable location
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    if exist "C:\Users\DELL\nodejs\node-v20.18.0-win-x64" (
        set "PATH=C:\Users\DELL\nodejs\node-v20.18.0-win-x64;%PATH%"
    )
)

:: Check Backend Virtualenv
if not exist "backend\.venv\Scripts\python.exe" (
    echo [INFO] Creating Python virtual environment in backend\.venv...
    python -m venv backend\.venv
    echo [INFO] Installing backend dependencies...
    backend\.venv\Scripts\pip install -r backend\requirements.txt
)

:: Check Frontend node_modules
if not exist "frontend\node_modules" (
    echo [INFO] Installing frontend dependencies...
    cd frontend
    npm install
    cd ..
)

echo [1/2] Launching SmartERP FastAPI Backend (http://localhost:8000)...
start "SmartERP - Backend API" powershell -NoExit -Command "cd '%ROOT_DIR%backend'; .\.venv\Scripts\activate; uvicorn app.main:app --reload --port 8000"

echo [2/2] Launching SmartERP React Frontend (http://localhost:5173)...
start "SmartERP - Frontend Web" powershell -NoExit -Command "cd '%ROOT_DIR%frontend'; $env:PATH = 'C:\Users\DELL\nodejs\node-v20.18.0-win-x64;' + $env:PATH; npm run dev"

echo.
echo ============================================================================
echo SmartERP successfully launched!
echo.
echo - Web Application: http://localhost:5173
echo - API Server:     http://localhost:8000
echo - Swagger Docs:   http://localhost:8000/docs
echo.
echo Demo Credentials:
echo   Administrator: admin / AdminPassword123!
echo   Manager:       manager / ManagerPassword123!
echo   Employee:      employee / EmployeePassword123!
echo ============================================================================
echo.
pause
