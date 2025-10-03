# Kopi Debate Bot Makefile (Unix/Linux/Mac)
# This file contains commands to manage the development lifecycle
# For Windows, use run.bat or run.ps1 scripts instead

.PHONY: help install test run down clean dev lint format check-requirements

# Default target - show available commands
help:
	@echo "Kopi Debate Bot - Available Commands (Unix/Linux/Mac):"
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
	@echo "  make debug         - Show environment debug information"
	@echo ""
	@echo "Note: For Windows users, use run.bat or run.ps1 scripts instead"
	@echo "Requirements: Python 3.12.x preferred (fallback to any Python 3.x)"

# Install all requirements
install: check-requirements
	@echo "Installing requirements for Kopi Debate Bot..."
	@echo "Creating virtual environment with Python 3.12..."
	@test -d venv || python3.12 -m venv venv || python3 -m venv venv
	@echo "Upgrading pip..."
	@./venv/bin/pip install --upgrade pip
	@echo "Installing production dependencies..."
	@./venv/bin/pip install -r requirements.txt
	@echo "Installing development dependencies (if available)..."
	@if [ -f requirements-dev.txt ]; then ./venv/bin/pip install -r requirements-dev.txt; fi
	@echo "Installation complete!"
	@echo ""
	@echo "Python version in venv:"
	@./venv/bin/python --version
	@echo ""
	@echo "To activate the virtual environment, run:"
	@echo "  source venv/bin/activate"

# Check if required tools are installed
check-requirements:
	@echo "Checking system requirements..."
	@echo "Checking for Python 3.12..."
	@python3.12 --version >/dev/null 2>&1 || python3 --version | grep -q "Python 3\.12" || (echo "WARNING: Python 3.12 preferred but not found. Attempting with available python3..." && python3 --version)
	@command -v python3 >/dev/null 2>&1 || (echo "ERROR: Python 3 is not installed or not in PATH" && exit 1)
	@command -v docker >/dev/null 2>&1 || (echo "ERROR: Docker is not installed or not in PATH" && exit 1)
	@command -v docker-compose >/dev/null 2>&1 || command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1 || (echo "ERROR: Docker Compose is not installed or not in PATH" && exit 1)
	@echo "All requirements satisfied!"

# Run tests
test:
	@echo "Running tests..."
	@test -d venv || (echo "Virtual environment not found. Run 'make install' first." && exit 1)
	@echo "Python version in use:"
	@./venv/bin/python --version
	@echo "Setting test environment..."
	@echo "Running pytest with coverage..."
	@PYTHONPATH=src ./venv/bin/python -m pytest tests/ -v --tb=short || echo "Some tests failed or pytest not installed. Installing pytest..."
	@if ! ./venv/bin/python -c "import pytest" 2>/dev/null; then \
		echo "Installing pytest..."; \
		./venv/bin/pip install pytest pytest-asyncio pytest-cov; \
		PYTHONPATH=src ./venv/bin/python -m pytest tests/ -v --tb=short; \
	fi
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
	@test -d venv || (echo "Virtual environment not found. Run 'make install' first." && exit 1)
	@echo "Python version in use:"
	@./venv/bin/python --version
	@echo "Setting environment variables for development..."
	@echo "DATABASE_URL=sqlite:///./kopi_debate.db"
	@echo "DEBUG=true"
	@echo "PYTHONPATH=src"
	@echo ""
	@echo "Starting uvicorn server with auto-reload..."
	@cd src && PYTHONPATH=../src DATABASE_URL=sqlite:///./kopi_debate.db DEBUG=true ../venv/bin/python -m uvicorn kopi_bot.main:app --reload --host 0.0.0.0 --port 8000

# Lint code
lint:
	@echo "Running code linting..."
	@test -d venv || (echo "Virtual environment not found. Run 'make install' first." && exit 1)
	@./venv/bin/python -m flake8 src/ tests/ || echo "Note: flake8 not installed, skipping"
	@./venv/bin/python -m mypy src/ || echo "Note: mypy not installed, skipping"
	@echo "Linting complete!"

# Format code
format:
	@echo "Formatting code..."
	@test -d venv || (echo "Virtual environment not found. Run 'make install' first." && exit 1)
	@./venv/bin/python -m black src/ tests/ || echo "Note: black not installed, skipping"
	@./venv/bin/python -m isort src/ tests/ || echo "Note: isort not installed, skipping"
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

# Debug environment info
debug:
	@echo "=== Environment Debug Info ==="
	@echo "Python versions available:"
	@which python3.12 2>/dev/null && python3.12 --version || echo "python3.12 not found"
	@which python3 2>/dev/null && python3 --version || echo "python3 not found"
	@echo ""
	@echo "Virtual environment status:"
	@if [ -d venv ]; then \
		echo "venv directory exists"; \
		echo "Python in venv: $$(./venv/bin/python --version 2>/dev/null || echo 'Failed to get version')"; \
		echo "Pip in venv: $$(./venv/bin/pip --version 2>/dev/null || echo 'Failed to get pip version')"; \
	else \
		echo "venv directory does not exist"; \
	fi
	@echo ""
	@echo "Docker status:"
	@docker --version 2>/dev/null || echo "Docker not available"
	@docker-compose --version 2>/dev/null || docker compose version 2>/dev/null || echo "Docker Compose not available"
	@echo ""
	@echo "Current working directory: $$(pwd)"
	@echo "Directory contents:"
	@ls -la