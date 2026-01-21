@echo off
REM TraceFinder Quick Start Script for Windows
REM This script helps you get started quickly

echo ============================================================
echo TraceFinder - Forensic Scanner Identification System
echo Quick Start Script
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [1/5] Python found!
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [2/5] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
) else (
    echo [2/5] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Create required directories
echo [5/5] Setting up directories...
if not exist "static\uploads" mkdir static\uploads
if not exist "models" mkdir models
echo Directories created!
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Starting TraceFinder application...
echo Press Ctrl+C to stop the server
echo.
echo The application will open at: http://localhost:5000
echo.

REM Start the application
python app.py

pause
