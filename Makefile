# Gatenet development Makefile

.PHONY: help venv install gatenet

help:
	@echo "Available targets:"
	@echo "  venv    - Create & source a Python virtual environment"
	@echo "  install - Install the package in the virtual environment"
	@echo "  gatenet - Run the gatenet CLI"

venv:
	python3 -m venv venv || true
	. venv/bin/activate

install: venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -e .

gatenet: venv
	@venv/bin/gatenet $(filter-out $@,$(MAKECMDGOALS))

%:
	@: