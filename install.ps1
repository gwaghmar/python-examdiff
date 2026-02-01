# Python ExamDiff Pro - Installation Script
# Run this script to set up the application

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Python ExamDiff Pro - Installation Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Found: $pythonVersion" -ForegroundColor Green
    
    # Extract version number
    $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
    if ($versionMatch) {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
            Write-Host "  ERROR: Python 3.11 or higher is required" -ForegroundColor Red
            Write-Host "  Please install Python from https://www.python.org/downloads/" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "  ERROR: Python not found" -ForegroundColor Red
    Write-Host "  Please install Python 3.11 or higher from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow

# Upgrade pip
Write-Host "  Upgrading pip..." -ForegroundColor Gray
python -m pip install --upgrade pip --quiet

# Install requirements
Write-Host "  Installing required packages..." -ForegroundColor Gray
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "  Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Creating directory structure..." -ForegroundColor Yellow

# Create necessary directories
$dirs = @(
    "resources",
    "resources\icons",
    "resources\themes"
)

foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Cyan
Write-Host "  GUI mode:        python main.py" -ForegroundColor White
Write-Host "  Compare files:   python main.py file1.txt file2.txt" -ForegroundColor White
Write-Host "  Compare dirs:    python main.py --dir folder1 folder2" -ForegroundColor White
Write-Host "  Help:            python main.py --help" -ForegroundColor White
Write-Host ""
Write-Host "For more information, see USAGE.md or README.md" -ForegroundColor Gray
Write-Host ""

# Ask if user wants to run the app now
$response = Read-Host "Would you like to run the application now? (Y/N)"
if ($response -eq 'Y' -or $response -eq 'y') {
    Write-Host ""
    Write-Host "Launching Python ExamDiff Pro..." -ForegroundColor Cyan
    python main.py
}
