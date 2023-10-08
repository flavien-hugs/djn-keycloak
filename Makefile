ifneq (,$(wildcard ./secrets/*.env))
    include ./secrets/*.env
    export
endif

COMPOSE_FILES := docker-compose.yaml
.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: run
run: ## Run
	docker compose up -d

.PHONY: restart
restart:	## restart one/all containers
	docker compose restart $(s)

.PHONY: stop
stop:	## Stop one/all containers
	docker compose stop

.PHONY: logs
logs: ## View logs from one/all containers
	docker compose logs -f $(s)

.PHONY: down
down: ## Stop the services, remove containers and networks
	docker compose down

.PHONY: destroy-all
destroy-all: ## destroy one/all images
	docker rmi -f $(docker images -a -q)
