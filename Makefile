THIS_FILE := $(lastword $(MAKEFILE_LIST))

## ---------
##	Container management
## ---------

create_containers: ## Create docker containers
	docker-compose up -d

destroy_containers: ## Destroy docker containers
	docker-compose down

start_containers: ## Start docker containers
	docker-compose start

stop_containers: ## Stop docker containers
	docker-compose stop

container_shell: ## Open an interactive shell in the main python container
	docker exec -it bingeable-py /bin/sh

## ---------
##	Testing
## ---------

test: test_py

test_py: flake8 bandit ## Run all python code tests (pylint, and bandit)

## ---------
##	Coding standards
## ---------

flake8: ## Check that python code complies with sylistic rules
	docker exec -it bingeable-py pdm run flake8

## ---------
##	Static analysis
## ---------

bandit: ## Check that python code passes bandit security analysis
	docker exec -it bingeable-py pdm run bandit -r ./

## ---------
##	Dependencies
## ---------

install_dependencies: pdm_install ## Install pdm packages

pdm_install: ## Install pdm packages
	docker exec -it bingeable-py pdm install

## ---------
##	Make setup
## ---------

_PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(THIS_FILE) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
