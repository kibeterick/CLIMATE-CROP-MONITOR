@echo off
color 0B
cls
echo.
echo  ========================================
echo   ADD YOUR FREE OPENWEATHERMAP API KEY
echo   Perfect for Student Projects!
echo  ========================================
echo.
echo  Your system works with demo data, but real weather
echo  data makes it much more impressive for your project!
echo.
echo  Don't have an API key yet?
echo  1. Go to: https://openweathermap.org/api
echo  2. Sign up FREE (no credit card needed)
echo  3. Get your API key from "My API Keys" section
echo  4. Come back here and enter it below
echo.
echo  ========================================
echo.
echo Current .env file:
type .env | findstr OPENWEATHER_API_KEY
echo.
echo ========================================
echo.
set /p api_key="Enter your FREE API key (or press Enter to skip): "

if "%api_key%"=="" (
    echo.
    echo No API key entered. Your system will use demo weather data.
    echo You can add the API key later by running this script again.
    echo.
    pause
    exit /b 0
)

echo.
echo Updating .env file with your API key...
powershell -Command "(Get-Content .env) -replace 'PUT_YOUR_FREE_API_KEY_HERE', '%api_key%' | Set-Content .env"

echo.
echo ========================================
echo SUCCESS! API Key Added Successfully!
echo ========================================
echo.
echo Your system will now use REAL weather data!
echo Perfect for impressing your professors! 
echo.
echo Updated .env file:
type .env | findstr OPENWEATHER_API_KEY
echo.
echo Next steps:
echo 1. Run your project: quick_start.bat
echo 2. Add farms with real locations
echo 3. See live weather data in your dashboard!
echo.
pause