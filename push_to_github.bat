@echo off
color 0A
cls
echo.
echo  ========================================
echo   PUSH TO GITHUB - Climate Crop Monitor
echo  ========================================
echo.
echo  This script will help you push your project to GitHub
echo.
echo  ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo Step 1: Initializing Git repository...
git init
if errorlevel 1 (
    echo Git already initialized or error occurred
)

echo.
echo Step 2: Adding all files...
git add .

echo.
echo Step 3: Creating initial commit...
git commit -m "Initial commit - Climate Crop Monitor v1.1.1"

echo.
echo ========================================
echo  GITHUB REPOSITORY SETUP
echo ========================================
echo.
echo Before continuing, you need to:
echo 1. Go to https://github.com/new
echo 2. Create a new repository named: climate-crop-monitor
echo 3. DO NOT initialize with README (we already have one)
echo 4. Copy the repository URL
echo.
echo Example URL: https://github.com/YOUR_USERNAME/climate-crop-monitor.git
echo.
set /p repo_url="Enter your GitHub repository URL: "

if "%repo_url%"=="" (
    echo.
    echo No URL entered. Exiting...
    echo Your code is committed locally. Run this script again when ready.
    pause
    exit /b 1
)

echo.
echo Step 4: Adding remote repository...
git remote add origin %repo_url%

echo.
echo Step 5: Pushing to GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo  PUSH FAILED - Possible Solutions:
    echo ========================================
    echo.
    echo 1. Authentication Error:
    echo    - Use GitHub Personal Access Token
    echo    - Go to: Settings  Developer settings  Personal access tokens
    echo.
    echo 2. Repository Already Exists:
    echo    - Use: git push -f origin main (force push)
    echo.
    echo 3. Remote Already Exists:
    echo    - Use: git remote set-url origin YOUR_URL
    echo    - Then run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  SUCCESS! Project Pushed to GitHub!
echo ========================================
echo.
echo Your Climate Crop Monitor is now on GitHub!
echo.
echo Repository URL: %repo_url%
echo.
echo Next steps:
echo 1. Visit your repository on GitHub
echo 2. Add a description and topics
echo 3. Share with your professors!
echo.
echo Useful Git commands:
echo - git status          (check status)
echo - git add .           (stage changes)
echo - git commit -m "msg" (commit changes)
echo - git push            (push to GitHub)
echo.
pause
