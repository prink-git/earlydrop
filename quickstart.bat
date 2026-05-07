@echo off
REM EarlyDrop Quick Start Script for Windows
REM This script helps you set up and run the EarlyDrop platform

cls
echo ========================================
echo Welcome to EarlyDrop Quick Start!
echo ========================================
echo.

REM Check if .env files exist
echo Checking configuration files...

if not exist "backend\.env" (
    echo ERROR: backend\.env not found
    echo Copy backend\.env.example to backend\.env and fill in your Supabase credentials
    pause
    exit /b 1
) else (
    echo [OK] backend\.env found
)

if not exist "frontend\.env.local" (
    echo Creating frontend\.env.local with default values...
    copy frontend\.env.example frontend\.env.local >nul
    echo [OK] frontend\.env.local created
) else (
    echo [OK] frontend\.env.local found
)

echo.
echo Setup Options:
echo 1. Install dependencies (recommended for first run)
echo 2. Start backend only
echo 3. Start frontend only
echo 4. Start both (requires two command prompts)
echo 5. Run integration tests
echo.
set /p choice="Select an option (1-5): "

if "%choice%"=="1" (
    echo.
    echo Installing backend dependencies...
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    cd ..
    
    echo.
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
    
    echo.
    echo [OK] Dependencies installed successfully!
) else if "%choice%"=="2" (
    echo.
    echo Starting backend...
    cd backend
    call venv\Scripts\activate.bat
    uvicorn main:app --reload
) else if "%choice%"=="3" (
    echo.
    echo Starting frontend...
    cd frontend
    call npm run dev
) else if "%choice%"=="4" (
    echo.
    echo To run both services, use two command prompts:
    echo.
    echo Command Prompt 1 ^(Backend^):
    echo   cd backend
    echo   venv\Scripts\activate.bat
    echo   uvicorn main:app --reload
    echo.
    echo Command Prompt 2 ^(Frontend^):
    echo   cd frontend
    echo   npm run dev
    echo.
    echo Backend: http://127.0.0.1:8000
    echo Frontend: http://localhost:3000
) else if "%choice%"=="5" (
    echo.
    echo Running integration tests...
    echo Make sure the backend is running first!
    echo.
    cd backend
    call venv\Scripts\activate.bat
    python integration_test.py
    pause
) else (
    echo Invalid option
    exit /b 1
)

echo.
echo Done!
pause
