# Kopi Debate Bot Makefile
# This file contains commands to manage the development lifecycle

.PHONY: help install test run down clean dev lint format check-requirements

# Default target - show available commands
help:
	@echo "Kopi Debate Bot - Available Commands:"
	@echo ""
	@echo "  make help          - Show this help message"
	@echo "  make install       - Install all requirements for running the service"
	@echo "  make test          - Run all tests"
	@echo "  make run           - Run the service and all related services in Docker"
	@echo "  make down          - Stop all running services"
	@echo "  make clean         - Stop and remove all containers, volumes, and images"
	@echo "  make dev           - Run the service in development mode (local)"
	@echo "  make lint          - Run code linting"
	@echo "  make format        - Format code using black and isort"
	@echo ""

# Install all requirements
install: check-requirements
	@echo "Installing requirements for Kopi Debate Bot..."
	@if not exist venv (python -m venv venv)
	@echo "Activating virtual environment and installing dependencies..."
	@venv\Scripts\pip install --upgrade pip
	@venv\Scripts\pip install -r requirements.txt
	@venv\Scripts\pip install -r requirements-dev.txt
	@echo "Installation complete!"
	@echo ""
	@echo "To activate the virtual environment, run:"
	@echo "  venv\Scripts\activate"

# Check if required tools are installed
check-requirements:
	@echo "Checking system requirements..."
	@python --version >nul 2>&1 || (echo "ERROR: Python is not installed or not in PATH" && exit 1)
	@docker --version >nul 2>&1 || (echo "ERROR: Docker is not installed or not in PATH" && exit 1)
	@docker-compose --version >nul 2>&1 || docker compose version >nul 2>&1 || (echo "ERROR: Docker Compose is not installed or not in PATH" && exit 1)
	@echo "All requirements satisfied!"

# Run tests
test:
	@echo "Running tests..."
	@if not exist venv (echo "Virtual environment not found. Run 'make install' first." && exit 1)
	@venv\Scripts\python -m pytest tests/ -v --cov=src/kopi_bot --cov-report=html --cov-report=term-missing
	@echo "Tests completed!"

# Run the service in Docker
run: check-requirements
	@echo "Starting Kopi Debate Bot services in Docker..."
	@docker-compose up --build -d
	@echo "Services are starting up..."
	@echo "API will be available at: http://localhost:8000"
	@echo "API documentation at: http://localhost:8000/docs"
	@echo ""
	@echo "To view logs, run: docker-compose logs -f"
	@echo "To stop services, run: make down"

# Stop services
down:
	@echo "Stopping all services..."
	@docker-compose down
	@echo "Services stopped!"

# Clean up everything
clean:
	@echo "Cleaning up all containers, volumes, and images..."
	@docker-compose down -v --rmi all --remove-orphans
	@echo "Cleanup complete!"

# Development mode (run locally)
dev: 
	@echo "Starting development server..."
	@if not exist venv (echo "Virtual environment not found. Run 'make install' first." && exit 1)
	@echo "Setting DATABASE_URL to SQLite for development..."
	@set DATABASE_URL=sqlite:///./kopi_debate.db&& set DEBUG=true&& venv\Scripts\python -m uvicorn kopi_bot.main:app --reload --host 0.0.0.0 --port 8000

# Lint code
lint:
	@echo "Running code linting..."
	@if not exist venv (echo "Virtual environment not found. Run 'make install' first." && exit 1)
	@venv\Scripts\python -m flake8 src/ tests/
	@venv\Scripts\python -m mypy src/
	@echo "Linting complete!"

# Format code
format:
	@echo "Formatting code..."
	@if not exist venv (echo "Virtual environment not found. Run 'make install' first." && exit 1)
	@venv\Scripts\python -m black src/ tests/
	@venv\Scripts\python -m isort src/ tests/
	@echo "Code formatting complete!"

# Show service logs
logs:
	@docker-compose logs -f

# Show service status
status:
	@docker-compose ps

# Build without cache
rebuild:
	@echo "Rebuilding services from scratch..."
	@docker-compose build --no-cache
	@echo "Rebuild complete!"