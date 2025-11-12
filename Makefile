# Enrich DDF Floor 2 - Makefile
# Development setup and execution commands

.PHONY: help install dev run frontend backend test clean lint

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Enrich DDF Floor 2 - Development Commands"
	@echo "========================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies
	@echo "📦 Installing backend dependencies..."
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements-minimal.txt
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ All dependencies installed"

dev: ## Run development environment (frontend + backend)
	@echo "🚀 Starting development environment..."
	@make backend & make frontend

run: ## Run full application (frontend + backend)
	@echo "🚀 Starting Enrich DDF Floor 2 Application..."
	@echo "Backend will start on http://localhost:8000"
	@echo "Frontend will start on http://localhost:5173"
	@echo "Press Ctrl+C to stop all services"
	@make backend & make frontend && wait

backend: ## Start backend server only
	@echo "🔧 Starting backend server..."
	bash workflows/run.sh --platform=local-macos --env=dev --verbose

frontend: ## Start frontend development server only
	@echo "🎨 Starting frontend development server..."
	cd frontend && npm run dev

test: ## Run all tests
	@echo "🧪 Running backend tests..."
	bash workflows/run.sh --test --verbose
	@echo "🧪 Running frontend tests..."
	cd frontend && npm run lint

build: ## Build frontend for production
	@echo "🏗️  Building frontend..."
	cd frontend && npm run build

clean: ## Clean build artifacts and dependencies
	@echo "🧹 Cleaning up..."
	rm -rf venv/
	rm -rf frontend/node_modules/
	rm -rf frontend/dist/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf __pycache__/
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleanup completed"

lint: ## Run linting for both frontend and backend
	@echo "🔍 Running linting..."
	@echo "Backend linting..."
	source venv/bin/activate && python -m ruff check .
	@echo "Frontend linting..."
	cd frontend && npm run lint

format: ## Format code for both frontend and backend
	@echo "🎨 Formatting code..."
	@echo "Backend formatting..."
	source venv/bin/activate && python -m ruff format .
	@echo "Frontend formatting..."
	cd frontend && npm run format || echo "No format script found in frontend"

check: ## Run full check suite (lint + test)
	@make lint
	@make test

status: ## Show application status
	@echo "📊 Application Status"
	@echo "===================="
	@echo "Python version: $(shell python3 --version)"
	@echo "Node version: $(shell node --version 2>/dev/null || echo 'Not installed')"
	@echo "npm version: $(shell npm --version 2>/dev/null || echo 'Not installed')"
	@echo "Virtual env: $(shell [ -d venv ] && echo 'Present' || echo 'Missing')"
	@echo "Frontend deps: $(shell [ -d frontend/node_modules ] && echo 'Installed' || echo 'Missing')"
	@echo "Backend port: 8000"
	@echo "Frontend port: 5173"

stop: ## Stop all running services
	@echo "🛑 Stopping all services..."
	@pkill -f "uvicorn" 2>/dev/null || echo "No uvicorn processes found"
	@pkill -f "vite" 2>/dev/null || echo "No vite processes found"
	@pkill -f "node.*vite" 2>/dev/null || echo "No node vite processes found"
	@echo "✅ All services stopped"

logs: ## Show logs (if any log files exist)
	@echo "📋 Recent logs..."
	@tail -n 20 *.log 2>/dev/null || echo "No log files found"

restart: stop run ## Restart the application

# Low-resource targets
frontend-low: ## Start frontend with lower memory usage
	@echo "🎨 Starting frontend (low-resource)..."
	cd frontend && NODE_OPTIONS=--max-old-space-size=1536 npm run dev

backend-low: ## Start backend without dev reload/timeouts
	@echo "🔧 Starting backend (low-resource)..."
	bash workflows/run.sh --platform=local-macos --env=dev --verbose --timeout=0

test-low: ## Run a lighter subset of tests with lower timeouts
	@echo "🧪 Running low-resource test suite..."
	bash tests/run_tests.sh --unit --fail-fast --timeout=120

# Docker Compose helpers
compose-validate: ## Validate compose.yml syntax
	@echo "🔎 Validating compose.yml..."
	docker compose -f compose.yml config --quiet

compose-up: ## Start minimal stack (profile: app)
	@echo "🚀 Starting Docker Compose (profile: app)..."
	docker compose --profile app up -d

compose-down: ## Stop all compose services
	@echo "🛑 Stopping Docker Compose services..."
	docker compose down

# Resource detection and adaptive testing
detect-resources: ## Detect available system resources
	@echo "🔍 Detecting system resources..."
	bash scripts/detect_resources.sh

detect-resources-json: ## Output resources as JSON
	@bash scripts/detect_resources.sh --format=json

test-auto: ## Run tests with auto-detected optimal settings
	@echo "🧪 Running tests with auto-detected settings..."
	@bash scripts/detect_resources.sh --apply --mode=balanced
	@npm test

test-auto-aggressive: ## Run tests with aggressive parallelization (if resources allow)
	@echo "⚡ Running tests with aggressive settings..."
	@bash scripts/detect_resources.sh --apply --mode=aggressive
	@npm test

test-auto-conservative: ## Run tests with conservative settings
	@echo "🛡️  Running tests with conservative settings..."
	@bash scripts/detect_resources.sh --apply --mode=conservative
	@npm test

playwright-auto: ## Update Playwright config based on available resources
	@echo "🎭 Updating Playwright config with detected resources..."
	@bash scripts/detect_resources.sh --update-playwright --mode=balanced

playwright-auto-aggressive: ## Update Playwright for maximum parallelization
	@echo "⚡ Updating Playwright for aggressive parallelization..."
	@bash scripts/detect_resources.sh --update-playwright --mode=aggressive
