THIS_FILE := $(lastword $(MAKEFILE_LIST))

## ---------
##	Docker images
## ---------

build_docker_image:
	docker build -t bingeable-py .

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

test_py: mypy flake8 bandit ## Run all python code tests (pylint, and bandit)

## ---------
##	Coding standards
## ---------

flake8: ## Check that python code complies with sylistic rules
	docker exec -it bingeable-py poetry run flake8

## ---------
##	Static analysis
## ---------

mypy: ## Check that python code passes type checking
	docker exec -it bingeable-py poetry run mypy --strict src/py/

bandit: ## Check that python code passes bandit security analysis
	docker exec -it bingeable-py poetry run bandit -r ./

## ---------
##	Dependencies
## ---------

install_dependencies: poetry_install ## Install poetry packages

poetry_install: ## Install poetry packages
	docker exec -it bingeable-py poetry install

## ---------
##	Make setup
## ---------

_PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(THIS_FILE) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
