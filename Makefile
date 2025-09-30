.PHONY: help install test lint format clean docker-build docker-up docker-down run

help:
	@echo "OpenGov-EarlyGerman - Development Commands"
	@echo ""
	@echo "install      Install dependencies"
	@echo "test         Run tests"
	@echo "test-cov     Run tests with coverage"
	@echo "lint         Run linters"
	@echo "format       Format code"
	@echo "clean        Clean build artifacts"
	@echo "docker-build Build Docker image"
	@echo "docker-up    Start Docker containers"
	@echo "docker-down  Stop Docker containers"
	@echo "run          Run FastAPI server"
	@echo "cli          Run CLI"

install:
	pip install -e ".[dev]"

test:
	pytest tests/

test-cov:
	pytest --cov=opengov_earlygerman --cov-report=html --cov-report=term-missing tests/

test-cov-100:
	pytest --cov=opengov_earlygerman --cov-report=term-missing --cov-fail-under=100 tests/

lint:
	ruff check opengov_earlygerman tests
	mypy opengov_earlygerman tests

format:
	black opengov_earlygerman tests
	ruff check --fix opengov_earlygerman tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

run:
	uvicorn opengov_earlygerman.api.main:app --reload --host 0.0.0.0 --port 8000

cli:
	python -m opengov_earlygerman.cli --help
