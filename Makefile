# Gatenet development Makefile

.PHONY: help venv install install-dev gatenet test test-cov clean

help:
	@echo "Available targets:"
	@echo "  venv    - Create & source a Python virtual environment"
	@echo "  install - Install the package in the virtual environment"
	@echo "  install-dev - Install the development dependencies"
	@echo "  gatenet - Run the gatenet CLI"
	@echo "  test    - Run tests using pytest"
	@echo "  test-cov - Run tests with coverage reporting"

# Create a Python virtual environment
venv:
	@test -d venv || python3 -m venv venv
	@venv/bin/python -m pip install --upgrade pip

# Install the package in editable mode
install: venv
	venv/bin/pip install -e .

# Install the package with development dependencies
install-dev: venv
	venv/bin/pip install -e ".[dev]"

# Run the gatenet CLI with passed arguments
gatenet:
	@venv/bin/gatenet $(filter-out $@,$(MAKECMDGOALS))

# Run tests using pytest
test:
	@venv/bin/pytest

# Run tests with coverage and fail on low coverage
test-cov:
	@venv/bin/pytest --cov=gatenet --cov-report=term-missing --cov-report=html --cov-fail-under=80 --maxfail=1 --disable-warnings -f

# Clean up the virtual environment and temporary files
clean:
	@rm -rf venv
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete
	@rm -rf .pytest_cache
	@rm -rf *.egg-info
	@rm -rf *coverage* .coverage htmlcov

# Ignore other targets
%:
	@:
