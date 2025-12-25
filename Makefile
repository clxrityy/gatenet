# Gatenet development Makefile

.PHONY: help venv install install-dev gatenet

help:
	@echo "Available targets:"
	@echo "  venv    - Create & source a Python virtual environment"
	@echo "  install - Install the package in the virtual environment"
  @echo "  install-dev - Install the development dependencies"
	@echo "  gatenet - Run the gatenet CLI"

venv:
	python3 -m venv venv || true
	. venv/bin/activate

install: venv
	venv/bin/pip install -e .

install-dev: venv
	venv/bin/pip install -e ".[dev]"

gatenet:
	@venv/bin/gatenet $(filter-out $@,$(MAKECMDGOALS))

%:
	@:
