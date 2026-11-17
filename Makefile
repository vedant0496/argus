.DEFAULT_GOAL := help
.PHONY: help install lint fmt typecheck test check infra up down logs

help: ## Show available targets
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: ## Install all workspace packages and dev tools
	uv sync --all-packages
	uv run pre-commit install

lint: ## Lint and check formatting
	uv run ruff check .
	uv run ruff format --check .

fmt: ## Auto-format and fix lint issues
	uv run ruff check --fix .
	uv run ruff format .

typecheck: ## Static type checking
	uv run mypy

test: ## Run the test suite with coverage
	uv run pytest --cov --cov-report=term-missing

check: lint typecheck test ## Everything CI runs

infra: ## Start Redpanda, TimescaleDB and Redis
	docker compose up -d --wait redpanda timescaledb redis console && docker compose up topics

up: ## Start infra and all services
	docker compose --profile apps up -d --build

down: ## Stop everything
	docker compose --profile apps down

logs: ## Tail service logs
	docker compose --profile apps logs -f --tail=100
