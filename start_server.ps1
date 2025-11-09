# Path Optimization - Quick Start Script
# Run this script to start the backend server

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Path Optimization - Backend Server" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Navigate to backend directory
Set-Location -Path $PSScriptRoot\backend

# Check if requirements are installed
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Yellow

$pipList = pip list 2>&1
$hasFlask = $pipList -match "Flask"
$hasNumpy = $pipList -match "numpy"

if (-not $hasFlask -or -not $hasNumpy) {
    Write-Host "Installing required packages..." -ForegroundColor Yellow
    pip install -r requirements.txt
} else {
    Write-Host "✓ All dependencies installed" -ForegroundColor Green
}

# Run tests (optional)
Write-Host ""
$runTests = Read-Host "Run tests before starting server? (y/N)"
if ($runTests -eq 'y' -or $runTests -eq 'Y') {
    Write-Host ""
    Write-Host "Running tests..." -ForegroundColor Yellow
    python test_optimizer.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "Tests failed! Check the errors above." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Start the server
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Starting Flask server..." -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server will be available at:" -ForegroundColor Green
Write-Host "  http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "To use the application:" -ForegroundColor Yellow
Write-Host "  1. Keep this server running" -ForegroundColor White
Write-Host "  2. Open frontend\index.html in your browser" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python server.py
