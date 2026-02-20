@echo off
echo ========================================
echo Climate Crop Monitor Setup
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing essential dependencies...
echo (This may take a while with slow internet connection)
pip install Django==4.2.7 requests python-dotenv Pillow --timeout 300
if errorlevel 1 (
    echo Error: Failed to install essential dependencies
    echo You can try again later or install manually
    pause
    exit /b 1
)

echo.
echo Installing optional analytics packages...
echo (pandas, numpy, scikit-learn - can be skipped if network is slow)
pip install pandas numpy scikit-learn --timeout 300
if errorlevel 1 (
    echo Warning: Optional packages failed to install
    echo The system will work without advanced analytics features
    echo You can install them later with: pip install pandas numpy scikit-learn
)

echo.
echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo Please edit .env file and add your OpenWeatherMap API key
)

echo.
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenWeatherMap API key
echo 2. Create superuser: python manage.py createsuperuser
echo 3. Run server: python manage.py runserver
echo.
pause
