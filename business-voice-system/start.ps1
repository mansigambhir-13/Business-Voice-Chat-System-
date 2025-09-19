# Quick Start Script for Voice System
param([string]$Mode = "streamlit")

Write-Host "🎯 Starting Stealth Business Voice System..." -ForegroundColor Cyan

switch ($Mode.ToLower()) {
    "streamlit" {
        Write-Host "🚀 Starting Streamlit at http://localhost:8501" -ForegroundColor Green
        .\venv\Scripts\Activate.ps1
        .\venv\Scripts\streamlit.exe run app.py
    }
    "api" {
        Write-Host "🚀 Starting API at http://localhost:5000" -ForegroundColor Green
        .\venv\Scripts\Activate.ps1
        .\venv\Scripts\python.exe api_integration.py
    }
    default {
        Write-Host "Usage: .\start.ps1 -Mode [streamlit|api]" -ForegroundColor Yellow
    }
}
