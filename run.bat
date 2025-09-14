@echo off
REM Kopi Debate Bot - Windows Batch Commands
REM Este archivo facilita la ejecución en Windows donde make no está disponible

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="test" goto test
if "%1"=="dev" goto dev
if "%1"=="run" goto run
if "%1"=="down" goto down
if "%1"=="clean" goto clean
goto help

:help
echo Kopi Debate Bot - Available Commands:
echo.
echo   run.bat help          - Show this help message
echo   run.bat install       - Install all requirements for running the service
echo   run.bat test          - Run all tests
echo   run.bat dev           - Run the service in development mode (local)
echo   run.bat run           - Run the service in Docker
echo   run.bat down          - Stop all running services
echo   run.bat clean         - Stop and remove all containers, volumes, and images
echo.
goto end

:install
echo Installing requirements for Kopi Debate Bot...
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
echo Activating virtual environment and installing dependencies...
venv\Scripts\pip install --upgrade pip
venv\Scripts\pip install -r requirements.txt
venv\Scripts\pip install -r requirements-dev.txt
echo Installation complete!
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate
goto end

:test
echo Running tests...
if not exist venv (
    echo Virtual environment not found. Run 'run.bat install' first.
    goto end
)
set PYTHONPATH=src
venv\Scripts\python -m pytest tests/ -v --cov=src/kopi_bot --cov-report=html --cov-report=term-missing
echo Tests completed!
goto end

:dev
echo Starting development server...
if not exist venv (
    echo Virtual environment not found. Run 'run.bat install' first.
    goto end
)
echo Setting up environment for development...
set PYTHONPATH=src
set DATABASE_URL=sqlite:///./kopi_debate.db
set DEBUG=true
venv\Scripts\python -m uvicorn kopi_bot.main:app --reload --host 0.0.0.0 --port 8000
goto end

:run
echo Starting Kopi Debate Bot services in Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    goto end
)
docker-compose --version >nul 2>&1
if errorlevel 1 (
    docker compose version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Docker Compose is not installed or not in PATH
        goto end
    )
)
docker-compose up --build -d
echo Services are starting up...
echo API will be available at: http://localhost:8000
echo API documentation at: http://localhost:8000/docs
echo.
echo To view logs, run: docker-compose logs -f
echo To stop services, run: run.bat down
goto end

:down
echo Stopping all services...
docker-compose down
echo Services stopped!
goto end

:clean
echo Cleaning up all containers, volumes, and images...
docker-compose down -v --rmi all --remove-orphans
echo Cleanup complete!
goto end

:end