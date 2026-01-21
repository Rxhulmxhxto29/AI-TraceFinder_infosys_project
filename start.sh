#!/bin/bash
# TraceFinder Quick Start Script for Linux/Mac
# This script helps you get started quickly

echo "============================================================"
echo "TraceFinder - Forensic Scanner Identification System"
echo "Quick Start Script"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/5] Python found!"
python3 --version
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[2/5] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created successfully!"
else
    echo "[2/5] Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo ""

# Install dependencies
echo "[4/5] Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "Dependencies installed successfully!"
echo ""

# Create required directories
echo "[5/5] Setting up directories..."
mkdir -p static/uploads
mkdir -p models
echo "Directories created!"
echo ""

echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo ""
echo "Starting TraceFinder application..."
echo "Press Ctrl+C to stop the server"
echo ""
echo "The application will open at: http://localhost:5000"
echo ""

# Start the application
python app.py
