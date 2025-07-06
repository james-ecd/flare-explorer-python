.PHONY: help install test lint format type-check security clean build publish

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	poetry install

test:  ## Run tests with coverage
	poetry run pytest --cov=flare_explorer --cov-report=term-missing --cov-report=xml

lint:  ## Run linting
	poetry run ruff check .

format:  ## Format code
	poetry run ruff format .

type-check:  ## Run type checking
	poetry run mypy flare_explorer/

security:  ## Run security scan
	poetry run bandit -r flare_explorer/

clean:  ## Clean build artifacts
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	poetry build

publish:  ## Publish to PyPI
	poetry publish

dev:  ## Install in development mode and run all checks
	$(MAKE) install
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) test
	$(MAKE) security

check:  ## Run all checks without stopping on failures
	-$(MAKE) format
	-$(MAKE) lint
	-$(MAKE) type-check
	-$(MAKE) test
	-$(MAKE) security