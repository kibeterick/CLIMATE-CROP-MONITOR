@echo off
:menu
cls
echo ========================================
echo Climate Crop Monitor - Management Menu
echo ========================================
echo.
echo 1. Start Development Server
echo 2. Run Migrations
echo 3. Create Superuser (Admin)
echo 4. Load Sample Data
echo 5. Update Weather Data
echo 6. Check System Status
echo 7. Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto start_server
if "%choice%"=="2" goto run_migrations
if "%choice%"=="3" goto create_superuser
if "%choice%"=="4" goto load_data
if "%choice%"=="5" goto update_weather
if "%choice%"=="6" goto check_status
if "%choice%"=="7" goto end
goto menu

:start_server
cls
echo Starting Development Server...
echo Press Ctrl+C to stop
echo.
venv\Scripts\python.exe manage.py runserver
pause
goto menu

:run_migrations
cls
echo Running Migrations...
venv\Scripts\python.exe manage.py migrate
echo.
pause
goto menu

:create_superuser
cls
echo Creating Superuser Account...
echo.
venv\Scripts\python.exe manage.py createsuperuser
echo.
pause
goto menu

:load_data
cls
echo Loading Sample Data...
venv\Scripts\python.exe manage.py seed_data
echo.
pause
goto menu

:update_weather
cls
echo Updating Weather Data...
venv\Scripts\python.exe manage.py update_weather
echo.
pause
goto menu

:check_status
cls
echo System Status Check...
echo.
echo Python Version:
venv\Scripts\python.exe --version
echo.
echo Installed Packages:
venv\Scripts\pip.exe list
echo.
echo Database Status:
if exist db.sqlite3 (
    echo Database: EXISTS
) else (
    echo Database: NOT FOUND - Run migrations!
)
echo.
pause
goto menu

:end
echo.
echo Goodbye!
exit /b 0
