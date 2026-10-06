@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Backend virtual environment not found.
    echo Create it and install dependencies from requirements.txt first.
    pause
    exit /b 1
)

set "DATABASE_URL=sqlite:///./smarterp_dev.db"
call ".venv\Scripts\activate.bat"

echo Applying local SQLite database migrations...
python -m alembic upgrade head
if errorlevel 1 (
    echo Database migration failed.
    pause
    exit /b 1
)

echo Seeding local authentication roles and development administrator...
python -m app.seed
if errorlevel 1 (
    echo Database seeding failed. Check ADMIN_PASSWORD in backend\.env.
    pause
    exit /b 1
)

echo Starting SmartERP API with local SQLite...
python -m uvicorn app.main:app --reload
