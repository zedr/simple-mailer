.PHONY: deps install clean tests serve

ENV=.env
PYTHON=python3.7
PYTHON_VERSION=$(shell ${PYTHON} -V | cut -d " " -f 2 | cut -c1-3)
SITE_PACKAGES=${ENV}/lib/python${PYTHON_VERSION}/site-packages
IN_ENV=source ${ENV}/bin/activate;

default: deps

${ENV}:
	@echo "Creating Python environment..." >&2
	@${PYTHON} -m venv ${ENV}
	@echo "Updating pip..." >&2
	@${IN_ENV} pip install -U pip

${SITE_PACKAGES}/poetry:
	@${IN_ENV} pip install poetry

deps: ${ENV} ${SITE_PACKAGES}/poetry
	@${IN_ENV} poetry install

${SITE_PACKAGES}/pytest.py:
	@${IN_ENV} pip install pytest

install: default
	@${IN_ENV} pip install -e .

serve: default
	@${IN_ENV} python main.py

tests: ${SITE_PACKAGES}/pytest.py
	@${IN_ENV} pytest src/simple_mailer/tests

clean:
	@rm -rf ${ENV} .env dist .pytest_cache