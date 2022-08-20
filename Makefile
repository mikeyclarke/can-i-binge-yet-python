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

test: test_py test_ts ## Run all code tests

test_py: mypy flake8 bandit pytest ## Run all python code tests

test_ts: jest ## Run all TypeScript code tests

## ---------
##	Coding standards
## ---------

flake8: ## Check that python code complies with sylistic rules
	docker exec -it bingeable-py poetry run flake8 src/py/ tests/py/

## ---------
##	Static analysis
## ---------

mypy: ## Check that python code passes type checking
	docker exec -it bingeable-py poetry run mypy --strict src/py/

bandit: ## Check that python code passes bandit security analysis
	docker exec -it bingeable-py poetry run bandit -r src/py

## ---------
##	Unit tests
## ---------

pytest: ## Run python unit tests
	docker exec -it bingeable-py poetry run pytest tests/py

jest: ## Run TypeScript unit tests
	docker exec -it bingeable-node yarn run jest --verbose --silent=false

## ---------
##	Dependencies
## ---------

install_dependencies: poetry_install ## Install poetry packages

poetry_install: ## Install poetry packages
	docker exec -it bingeable-py poetry install

## ---------
##	Asset compilation
## ---------

webpack_watch: ## Have webpack watch source files and re-compile assets on change
	docker exec -it bingeable-node yarn run webpack --watch --config webpack.dev.js

webpack_compile: ## Have webpack execute a one-off asset compilation
	docker exec -it bingeable-node yarn run webpack --config webpack.dev.js

## ---------
##	Make setup
## ---------

_PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(THIS_FILE) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
