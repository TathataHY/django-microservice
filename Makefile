.PHONY: help build up down logs test fmt lint migrate load-data clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build Docker images
	docker-compose build

up: ## Start services
	docker-compose up -d

down: ## Stop services
	docker-compose down

logs: ## Show logs
	docker-compose logs -f web

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage report
	pytest --cov=api --cov=health --cov-report=html --cov-report=term-missing

fmt: ## Format code with black
	black .

lint: ## Lint code with ruff
	ruff check .

lint-fix: ## Lint and fix code with ruff
	ruff check --fix .

migrate: ## Run migrations
	python manage.py migrate

makemigrations: ## Create migrations
	python manage.py makemigrations

load-data: ## Load sample data (if exists)
	@echo "No sample data script yet"

clean: ## Clean up generated files
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build

install: ## Install dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt

shell: ## Open Django shell
	python manage.py shell

superuser: ## Create superuser
	python manage.py createsuperuser

docker-test: ## Run tests in Docker
	docker-compose run --rm web pytest

docker-lint: ## Run linter in Docker
	docker-compose run --rm web ruff check .

docker-fmt: ## Format code in Docker
	docker-compose run --rm web black .

docker-migrate: ## Run migrations in Docker
	docker-compose run --rm web python manage.py migrate

docker-makemigrations: ## Create migrations in Docker
	docker-compose run --rm web python manage.py makemigrations

