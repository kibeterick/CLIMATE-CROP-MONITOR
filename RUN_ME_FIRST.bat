@echo off
color 0A
cls
echo.
echo  ========================================================
echo   CLIMATE CROP MONITOR v1.1.1
echo   Kisii University - ARON SIGEI (IN13/00030/21)
echo  ========================================================
echo.
echo   DATABASE MIGRATION ISSUES FIXED!
echo.
echo  ========================================================
echo.
echo   CHOOSE YOUR SETUP METHOD:
echo.
echo   1. QUICK START (Recommended - 2 minutes)
echo      - Installs essential packages only
echo      - Works great with slow internet
echo      - Gets you running fast!
echo.
echo   2. FULL SETUP (5-10 minutes)
echo      - Installs all packages including analytics
echo      - Requires good internet connection
echo      - Includes advanced features
echo.
echo   3. JUST RUN MIGRATIONS (if packages already installed)
echo      - Only sets up database
echo      - Fastest option
echo.
echo   4. MANAGEMENT MENU
echo      - Interactive menu for all tasks
echo      - Start server, create users, etc.
echo.
echo   5. READ INSTRUCTIONS
echo      - Open START_HERE.txt
echo.
echo   6. EXIT
echo.
echo  ========================================================
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo.
    echo Starting Quick Setup...
    call quick_start.bat
    goto end
)

if "%choice%"=="2" (
    echo.
    echo Starting Full Setup...
    call setup.bat
    goto end
)

if "%choice%"=="3" (
    echo.
    echo Running Migrations...
    call run_migrations.bat
    goto end
)

if "%choice%"=="4" (
    echo.
    echo Opening Management Menu...
    call manage_system.bat
    goto end
)

if "%choice%"=="5" (
    echo.
    echo Opening Instructions...
    start notepad START_HERE.txt
    pause
    goto end
)

if "%choice%"=="6" (
    goto end
)

echo Invalid choice! Please run the script again.
pause

:end
exit /b 0
