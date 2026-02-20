@echo off
echo ========================================
echo Climate Crop Monitor - Database Setup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv\Scripts\python.exe (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

echo Step 1: Running migrations...
venv\Scripts\python.exe manage.py migrate

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Migration failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Database is ready.
echo ========================================
echo.
echo Next steps:
echo 1. Create a superuser: venv\Scripts\python.exe manage.py createsuperuser
echo 2. Load sample data: venv\Scripts\python.exe manage.py seed_data
echo 3. Start server: venv\Scripts\python.exe manage.py runserver
echo.
pause
