@echo off
echo ========================================
echo Climate Crop Monitor - Apply Enhancements
echo Version 1.1.0
echo ========================================
echo.

echo [1/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

echo [2/4] Applying database migrations...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Migration failed!
    pause
    exit /b 1
)

echo.
echo [3/4] Updating weather data for all farms...
python manage.py update_weather --force
if errorlevel 1 (
    echo WARNING: Weather update had some errors (this is normal if no API key is set)
)

echo.
echo [4/4] Collecting static files...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo WARNING: Static files collection had issues
)

echo.
echo ========================================
echo ✓ Enhancements Applied Successfully!
echo ========================================
echo.
echo New Features Available:
echo - Data Export (CSV)
echo - Batch Operations
echo - Farm Statistics Dashboard
echo - Enhanced Predictions
echo - Automated Alerts
echo - Search and Filter
echo.
echo Quick Start:
echo 1. python manage.py runserver
echo 2. Visit http://127.0.0.1:8000/
echo 3. Check Dashboard for new buttons
echo.
echo For details, see ENHANCEMENTS.md
echo.
pause
