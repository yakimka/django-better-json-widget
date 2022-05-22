SHELL:=/usr/bin/env bash

SRC_DIR=.

.PHONY: all
all: help

.PHONY: lint
lint:  ## Run flake8, mypy, other linters and verify formatting
	make flake8
	make mypy
	make verify_format
	poetry run doc8 -q docs
	poetry run yamllint -s .

.PHONY: flake8
flake8:  ## Run flake8
	poetry run flake8 $(SRC_DIR)

.PHONY: mypy
mypy:  ## Run mypy
	poetry run mypy $(SRC_DIR)

.PHONY: unit
unit:  ## Run unit tests
	poetry run pytest

.PHONY: package
package:  ## Run packages (dependencies) checks
	poetry check
	poetry run pip check
	poetry run safety check --full-report

.PHONY: test
test: lint package unit  ## Run linting and tests

.PHONY: format
format:  ## Format python files with black and isort
	poetry run black --preview $(SRC_DIR)
	poetry run isort $(SRC_DIR)


.PHONY: verify_format
verify_format:  ## Verify python files formatting with black and isort
	poetry run black --preview --check --diff $(SRC_DIR)
	poetry run isort --check-only --diff $(SRC_DIR)


.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
