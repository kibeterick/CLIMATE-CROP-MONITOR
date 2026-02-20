@echo off
echo ========================================
echo Climate Crop Monitor - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv\Scripts\python.exe (
    echo Virtual environment not found. Installing essential packages only...
    echo.
    
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    
    echo Installing essential packages (Django, requests, python-dotenv, Pillow)...
    venv\Scripts\pip.exe install Django==4.2.7 requests python-dotenv Pillow --timeout 300
    if errorlevel 1 (
        echo ERROR: Failed to install packages
        pause
        exit /b 1
    )
    
    echo.
    echo Essential packages installed successfully!
    echo Note: Advanced analytics features (pandas, numpy, scikit-learn) not installed.
    echo You can install them later when you have better internet connection.
    echo.
)

echo Checking database...
if not exist db.sqlite3 (
    echo Database not found. Running migrations...
    venv\Scripts\python.exe manage.py migrate
    if errorlevel 1 (
        echo ERROR: Migration failed!
        pause
        exit /b 1
    )
    echo.
    echo Database created successfully!
    echo.
) else (
    echo Database found. Applying any pending migrations...
    venv\Scripts\python.exe manage.py migrate
)

echo.
echo ========================================
echo Starting Development Server...
echo ========================================
echo.
echo Server will start at: http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
echo.
echo IMPORTANT: Create your first account at /register
echo.
pause

venv\Scripts\python.exe manage.py runserver
