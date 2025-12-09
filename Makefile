# Makefile for AI Tutor RAG System

.PHONY: help install install-dev test lint format clean build run docker-up docker-down

help:
	@echo "AI Tutor RAG System - Available Commands"
	@echo "========================================"
	@echo "make install       - Install dependencies"
	@echo "make install-dev   - Install dev dependencies"
	@echo "make test          - Run tests"
	@echo "make lint          - Run linter"
	@echo "make format        - Format code with black"
	@echo "make clean         - Clean up temporary files"
	@echo "make build         - Build Docker images"
	@echo "make run           - Run the application"
	@echo "make docker-up     - Start Docker containers"
	@echo "make docker-down   - Stop Docker containers"

install:
	cd backend && pip install -r requirements.txt

install-dev:
	cd backend && pip install -r requirements.txt -r requirements_dev.txt

test:
	cd backend && pytest tests/ -v

lint:
	cd backend && flake8 . --max-line-length=100 && mypy . --ignore-missing-imports

format:
	cd backend && black . && isort .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

build:
	docker-compose build

run:
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down
