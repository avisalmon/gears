# GearLab — One-click launcher
# Usage: .\run.ps1
# This script activates the virtualenv and launches GearLab.

$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot

Set-Location $projectRoot

# Create venv if missing
if (-not (Test-Path "env\Scripts\Activate.ps1")) {
    Write-Host "[GearLab] Creating virtualenv..." -ForegroundColor Cyan
    python -m venv env
}

# Activate
Write-Host "[GearLab] Activating virtualenv..." -ForegroundColor Cyan
& ".\env\Scripts\Activate.ps1"

# Install/verify dependencies
Write-Host "[GearLab] Checking dependencies..." -ForegroundColor Cyan
$env:HTTP_PROXY  = "http://proxy-mu.intel.com:912"
$env:HTTPS_PROXY = "http://proxy-mu.intel.com:912"
pip install -r requirements.txt --quiet

# Launch
Write-Host "[GearLab] Launching..." -ForegroundColor Green
python main.py
