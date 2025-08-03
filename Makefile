# Gatenet Project Makefile

.PHONY: help venv install test coverage badge docs clean build publish release

help:
	@echo "Gatenet Makefile targets:"
	@echo "  venv      - Create a virtual environment (venv/)"
	@echo "  install   - Install all dependencies (including dev and docs)"
	@echo "  test      - Run all tests with pytest"
	@echo "  coverage  - Run tests and generate HTML and XML coverage reports"
	@echo "  badge     - Generate a coverage badge (SVG)"
	@echo "  docs      - Build Sphinx documentation (HTML)"
	@echo "  clean     - Remove build, dist, coverage, and doc artifacts"
	@echo "  build     - Build the package (wheel and sdist)"
	@echo "  publish   - Upload to PyPI (testpypi if TESTPYPI=1)"
	@echo "  release   - Run build, test, docs, and publish for release"

venv:
	python3 -m venv venv
	@echo "Run: source venv/bin/activate"

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r docs/requirements.txt || true


# Install test package
install-test:
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps gatenet

# Run all tests

test:
	pytest

# Run tests and generate coverage reports
coverage:
	pytest --cov=src/gatenet --cov-report=xml --cov-report=html

# Copy HTML coverage report into docs static directory
coverage-copy:
	rm -rf docs/source/_static/htmlcov
	mkdir -p docs/source/_static/htmlcov
	@if command -v rsync >/dev/null 2>&1; then \
		rsync -a htmlcov/ docs/source/_static/htmlcov/; \
	else \
		cp -R htmlcov/. docs/source/_static/htmlcov/; \
	fi

# Generate a coverage badge (SVG)
badge:
	rm -f docs/source/_static/coverage.svg
	coverage-badge -o docs/source/_static/coverage.svg

# Generate a coverage summary table for docs
coverage-summary:
	python3 docs/source/gen_coverage_table.py

# Generate Sphinx documentation
docs-copy: 
	sphinx-apidoc -o docs/source/ src/gatenet

# Build Sphinx documentation (HTML)
docs: coverage coverage-copy badge coverage-summary docs-copy
	cd docs && make html

# Publish docs to readthedocs.io
docs-build: venv
	sphinx-build -b html docs/source docs/build/html

	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov
	rm -rf docs/build docs/source/_static/htmlcov docs/source/_static/coverage.svg

# Delete all empty files in the project
delete-empty:
	python3 scripts/delete_empty_files.py

# Clean build, dist, coverage, and doc artifacts
clean:
	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov
	rm -rf docs/build docs/source/_static/htmlcov docs/source/_static/coverage.svg

# Build the package (wheel and sdist)
build:
	python3 -m build

# Publish to PyPI or TestPyPI
publish:
ifeq ($(TESTPYPI),1)
	python3 -m twine upload --repository testpypi dist/*
else
	python3 -m twine upload dist/*
endif

# Full release: build, test, docs, publish
release: clean build test docs publish
	@echo "Release complete!"

# Show and update project version in pyproject.toml and docs/source/conf.py
version:
	@echo "Current version in pyproject.toml: $$(grep '^[[:space:]]*version' pyproject.toml | head -1 | sed -E 's/^[[:space:]]*version[[:space:]]*=[[:space:]]*[\"'\'']([^\"'\'']+)[\"'\''].*/\1/')"
	@echo "Current version in docs/source/conf.py: $$(grep '^[[:space:]]*release' docs/source/conf.py | head -1 | sed -E "s/^[[:space:]]*release[[:space:]]*=[[:space:]]*['\"]([^'\"]+)['\"].*/\1/")"
	@read -p "Enter new version (or leave blank to skip): " v; \
	if [ "$$v" != "" ]; then \
		sed -i '' -E "s/^[[:space:]]*version[[:space:]]*=[[:space:]]*[\"'\''][^\"'\'']*[\"'\'']/version = \"$$v\"/" pyproject.toml; \
		sed -i '' -E "s/^[[:space:]]*release[[:space:]]*=[[:space:]]*['\"][^'\"]*['\"]/release = '$$v'/" docs/source/conf.py; \
		echo "Updated version to $$v in pyproject.toml and docs/source/conf.py"; \
	else \
		echo "No version change."; \
	fi
