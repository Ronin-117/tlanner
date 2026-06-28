# Tlanner — Developer Commands
# Usage: make <target>

COMPOSE_BASE = docker compose -f infra/docker-compose.yml
COMPOSE_DEV  = $(COMPOSE_BASE) -f infra/docker-compose.dev.yml
ENV_FILE     = --env-file .env

# ─── Infrastructure ────────────────────────────────────────────────────────────

.PHONY: dev-infra
dev-infra: ## Start all infrastructure containers (dev mode with ports exposed)
	$(COMPOSE_DEV) $(ENV_FILE) up -d

.PHONY: infra-logs
infra-logs: ## Tail logs from all infra containers
	$(COMPOSE_DEV) $(ENV_FILE) logs -f

.PHONY: down
down: ## Stop and remove all containers (keeps volumes)
	$(COMPOSE_DEV) $(ENV_FILE) down

.PHONY: down-volumes
down-volumes: ## Stop containers AND delete all data volumes (full reset)
	$(COMPOSE_DEV) $(ENV_FILE) down -v

.PHONY: ps
ps: ## Show running containers and their status
	$(COMPOSE_DEV) $(ENV_FILE) ps

# ─── Individual service logs ───────────────────────────────────────────────────

.PHONY: logs-postgres
logs-postgres:
	$(COMPOSE_DEV) $(ENV_FILE) logs -f postgres

.PHONY: logs-redis
logs-redis:
	$(COMPOSE_DEV) $(ENV_FILE) logs -f redis

.PHONY: logs-rabbit
logs-rabbit:
	$(COMPOSE_DEV) $(ENV_FILE) logs -f rabbitmq

# ─── Utilities ─────────────────────────────────────────────────────────────────

.PHONY: psql
psql: ## Open a psql shell inside the postgres container
	docker exec -it tlanner-postgres psql -U tlanner -d tlanner_db

.PHONY: redis-cli
redis-cli: ## Open a redis-cli shell
	docker exec -it tlanner-redis redis-cli

.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help