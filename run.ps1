# Kopi Debate Bot - PowerShell Commands
# Este archivo facilita la ejecución en Windows con PowerShell

param(
    [Parameter(Mandatory=$false)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Kopi Debate Bot - Available Commands:" -ForegroundColor Green
    Write-Host ""
    Write-Host "  .\run.ps1 help          - Show this help message"
    Write-Host "  .\run.ps1 install       - Install all requirements for running the service"
    Write-Host "  .\run.ps1 test          - Run all tests"
    Write-Host "  .\run.ps1 dev           - Run the service in development mode (local)"
    Write-Host "  .\run.ps1 run           - Run the service in Docker"
    Write-Host "  .\run.ps1 down          - Stop all running services"
    Write-Host "  .\run.ps1 clean         - Stop and remove all containers, volumes, and images"
    Write-Host ""
}

function Install-Dependencies {
    Write-Host "Installing requirements for Kopi Debate Bot..." -ForegroundColor Green
    
    if (!(Test-Path "venv")) {
        Write-Host "Creating virtual environment..."
        python -m venv venv
    }
    
    Write-Host "Activating virtual environment and installing dependencies..."
    & "venv\Scripts\pip" install --upgrade pip
    & "venv\Scripts\pip" install -r requirements.txt
    & "venv\Scripts\pip" install -r requirements-dev.txt
    
    Write-Host "Installation complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To activate the virtual environment, run:"
    Write-Host "  venv\Scripts\Activate.ps1"
}

function Run-Tests {
    Write-Host "Running tests..." -ForegroundColor Green
    
    if (!(Test-Path "venv")) {
        Write-Host "Virtual environment not found. Run '.\run.ps1 install' first." -ForegroundColor Red
        return
    }
    
    $env:PYTHONPATH = "src"
    & "venv\Scripts\python" -m pytest tests/ -v --cov=src/kopi_bot --cov-report=html --cov-report=term-missing
    Write-Host "Tests completed!" -ForegroundColor Green
}

function Start-DevServer {
    Write-Host "Starting development server..." -ForegroundColor Green
    
    if (!(Test-Path "venv")) {
        Write-Host "Virtual environment not found. Run '.\run.ps1 install' first." -ForegroundColor Red
        return
    }
    
    Write-Host "Setting up environment for development..."
    $env:PYTHONPATH = "src"
    $env:DATABASE_URL = "sqlite:///./kopi_debate.db"
    $env:DEBUG = "true"
    
    & "venv\Scripts\python" -m uvicorn kopi_bot.main:app --reload --host 0.0.0.0 --port 8000
}

function Start-Docker {
    Write-Host "Starting Kopi Debate Bot services in Docker..." -ForegroundColor Green
    
    # Check if Docker is installed
    try {
        docker --version | Out-Null
    } catch {
        Write-Host "ERROR: Docker is not installed or not in PATH" -ForegroundColor Red
        return
    }
    
    # Check if Docker Compose is installed
    try {
        docker-compose --version | Out-Null
    } catch {
        try {
            docker compose version | Out-Null
        } catch {
            Write-Host "ERROR: Docker Compose is not installed or not in PATH" -ForegroundColor Red
            return
        }
    }
    
    docker-compose up --build -d
    Write-Host "Services are starting up..." -ForegroundColor Green
    Write-Host "API will be available at: http://localhost:8000" -ForegroundColor Yellow
    Write-Host "API documentation at: http://localhost:8000/docs" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To view logs, run: docker-compose logs -f"
    Write-Host "To stop services, run: .\run.ps1 down"
}

function Stop-Services {
    Write-Host "Stopping all services..." -ForegroundColor Green
    docker-compose down
    Write-Host "Services stopped!" -ForegroundColor Green
}

function Clean-All {
    Write-Host "Cleaning up all containers, volumes, and images..." -ForegroundColor Green
    docker-compose down -v --rmi all --remove-orphans
    Write-Host "Cleanup complete!" -ForegroundColor Green
}

# Main execution
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "install" { Install-Dependencies }
    "test" { Run-Tests }
    "dev" { Start-DevServer }
    "run" { Start-Docker }
    "down" { Stop-Services }
    "clean" { Clean-All }
    default { 
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Show-Help 
    }
}