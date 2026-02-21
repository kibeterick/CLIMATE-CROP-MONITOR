@echo off
echo ========================================
echo Climate Crop Monitor - System Update
echo Version 2.1.0
echo ========================================
echo.
echo Student: ARON SIGEI (IN13/00030/21)
echo Supervisor: Dr. Tombe
echo Institution: Kisii University
echo.
echo ========================================
echo This will update your system with:
echo - Climate Classification features
echo - Soil Analysis features
echo ========================================
echo.
pause

echo.
echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [2/3] Running database migrations...
python manage.py migrate

echo.
echo [3/3] Checking for errors...
python manage.py check

echo.
echo ========================================
echo Update Complete!
echo ========================================
echo.
echo NEW FEATURES AVAILABLE:
echo.
echo 1. CLIMATE CLASSIFICATION
echo    - Detect desert/arid zones
echo    - Get crop recommendations
echo    - Plan irrigation needs
echo.
echo 2. SOIL ANALYSIS
echo    - Test pH and NPK levels
echo    - Get fertilizer recommendations
echo    - Track soil health over time
echo.
echo ========================================
echo.
echo QUICK START:
echo 1. Run: quick_start.bat
echo 2. Login to your account
echo 3. Try "Location Weather" for climate analysis
echo 4. Try "Soil Analysis" on any farm
echo.
echo DOCUMENTATION:
echo - NEW_FEATURES_GUIDE.md (Quick guide)
echo - CLIMATE_SOIL_FEATURES.md (Full guide)
echo - CHANGELOG.md (What changed)
echo.
echo ========================================
pause
