@echo off
echo ============================================
echo   Path Optimization - Backend Server
echo ============================================
echo.

cd backend

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo Error: Python not found! Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo.
echo Installing/checking dependencies...
pip install -r requirements.txt

echo.
echo ============================================
echo Starting Flask server...
echo ============================================
echo.
echo Server will be available at:
echo   http://localhost:5000
echo.
echo To use the application:
echo   1. Keep this server running
echo   2. Open frontend\index.html in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

python server.py
pause
