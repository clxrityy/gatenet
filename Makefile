# Gatenet development Makefile

.PHONY: help venv install install-dev gatenet test test-cov clean lint format

BIN := venv/bin
PYTHON := $(BIN)/python
PIP := $(BIN)/pip
RUFF := $(BIN)/ruff
PYTEST := $(BIN)/pytest
GATENET := $(BIN)/gatenet
PRE-COMMIT := $(BIN)/pre-commit

help:
	@echo "Available targets:"
	@echo "  venv    - Create & source a Python virtual environment"
	@echo "  install - Install the package in the virtual environment"
	@echo "  install-dev - Install the development dependencies"
	@echo "  gatenet - Run the gatenet CLI"
	@echo "  test    - Run tests using pytest"
	@echo "  test-cov - Run tests with coverage reporting"
	@echo "  clean   - Remove virtual environment and temporary files"
	@echo "  lint    - Check code style with ruff"
	@echo "  lint-fix - Fix code style issues with ruff"
	@echo "  format  - Format code with ruff"

# Create a Python virtual environment
venv:
	@test -d venv || python3 -m venv venv
	@venv/bin/python -m pip install --upgrade pip

# Install the package in editable mode
install: venv
	$(PIP) install -e .

# Install the package with development dependencies
install-dev: venv
	$(PIP) install -e ".[dev]"
	$(PRE-COMMIT) install

# Run the gatenet CLI with passed arguments
gatenet:
	@$(GATENET) $(filter-out $@,$(MAKECMDGOALS))

# Run tests using pytest
test:
	@$(PYTEST)

# Run tests with coverage and fail on low coverage
test-cov:
	@$(PYTEST) --cov=gatenet --cov-report=term-missing --cov-report=html --cov-fail-under=80 --maxfail=1 --disable-warnings -f

# Clean up the virtual environment and temporary files
clean:
	@rm -rf venv
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete
	@rm -rf .pytest_cache
	@rm -rf *.egg-info
	@rm -rf *coverage* .coverage htmlcov *cache

# Check code style with ruff
lint:
	@$(RUFF) check

# Fix code style issues with ruff
lint-fix:
	@$(RUFF) check --fix

# Format code with ruff
format:
	@$(RUFF) format

# Ignore other targets
%:
	@:
