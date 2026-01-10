# Gatenet development Makefile

.PHONY: help venv install install-dev gatenet test test-cov clean lint format docs-build docs-deploy-version docs-deploy-dev docs-set-default check-version

BIN := venv/bin
PYTHON := $(BIN)/python
PIP := $(BIN)/pip
RUFF := $(BIN)/ruff
PYTEST := $(BIN)/pytest
GATENET := $(BIN)/gatenet
PRE-COMMIT := $(BIN)/pre-commit
DOCS := $(BIN)/mkdocs
MIKE := $(BIN)/mike
PRINTF_FORMAT := "  %-25s %s\n"
PYPROJECT := pyproject.toml

help:
	@echo "Available targets:"
	@printf $(PRINTF_FORMAT) "venv" "Create & source a Python virtual environment"
	@printf $(PRINTF_FORMAT) "install" "Install the package in the virtual environment"
	@printf $(PRINTF_FORMAT) "install-dev" "Install the development dependencies"
	@printf $(PRINTF_FORMAT) "gatenet" "Run the gatenet CLI"
	@printf $(PRINTF_FORMAT) "test" "Run tests using pytest"
	@printf $(PRINTF_FORMAT) "test-cov" "Run tests with coverage reporting"
	@printf $(PRINTF_FORMAT) "clean" "Remove virtual environment and temporary files"
	@printf $(PRINTF_FORMAT) "lint" "Check code style with ruff"
	@printf $(PRINTF_FORMAT) "lint-fix" "Fix code style issues with ruff"
	@printf $(PRINTF_FORMAT) "format" "Format code with ruff"
	@printf $(PRINTF_FORMAT) "docs-build" "Build the documentation"
	@printf $(PRINTF_FORMAT) "docs-deploy-version" "Deploy documentation for the current version"
	@printf $(PRINTF_FORMAT) "docs-deploy-dev" "Deploy documentation to the 'dev' version"
	@printf $(PRINTF_FORMAT) "docs-set-default" "Set the default documentation version to 'latest'"
	@printf $(PRINTF_FORMAT) "check-version" "Check if Git tag version matches pyproject.toml version"

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
	$(PIP) install -e ".[docs]"
	$(PRE-COMMIT) install

# Run the gatenet CLI with passed arguments
gatenet:
	@$(GATENET) $(ARGS) || true

# Run tests using pytest
test:
	@$(PYTEST)
	@$(PYTHON) scripts/coverage_summary.py

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
	@rm -rf *coverage* .coverage htmlcov *cache site/ .ruff_cache

# Check code style with ruff
lint:
	@$(RUFF) check
	@$(PYTHON) scripts/lint_docs.py

# Fix code style issues with ruff
lint-fix:
	@$(RUFF) check --fix

# Format code with ruff
format:
	@$(RUFF) format

# Local dev docs preview
docs-dev: test
	@$(DOCS) serve

# Build the documentation for dev version
docs-dev-build:
	@$(DOCS) build --site-dir site-dev

# Build the documentation using mkdocs
docs-build: test
	@$(DOCS) build

# Deploy the documentation for the current version
docs-deploy-version:
	@$(MIKE) deploy --update-aliases $(VERSION) latest

# Deploy the documentation to the 'dev' version
docs-deploy-dev:
	@$(MIKE) deploy --push dev

# Set the default documentation version to 'latest'
docs-set-default:
	@$(MIKE) set-default latest

# Check if Git tag version matches pyproject.toml version
check-version:
	@$(PYTHON) scripts/check_version.py

# Ignore other targets
%:
	@:
