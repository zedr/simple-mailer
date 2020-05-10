.PHONY: deps install clean lint tests serve sdist wheel

ENV=.env
PYTHON=python3.7
PYTHON_VERSION=$(shell ${PYTHON} -V | cut -d " " -f 2 | cut -c1-3)
SITE_PACKAGES=${ENV}/lib/python${PYTHON_VERSION}/site-packages
IN_ENV=source ${ENV}/bin/activate;
SRC_PATH=src/simple_mailer

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

lint: ${ENV}
	# Mypy informs only and does not break the build.
	@${IN_ENV} mypy ${SRC_PATH} || true
	@${IN_ENV} flake8 ${SRC_PATH}
	@${IN_ENV} black ${SRC_PATH}

tests: ${ENV} ${SITE_PACKAGES}/pytest.py
	@${IN_ENV} pytest src/simple_mailer/tests

sdist: ${ENV}
	@${IN_ENV} python setup.py sdist

wheel: ${ENV}
	@${IN_ENV} python setup.py bdist_wheel

clean_dist:
	@rm -rf dist

clean: clean_dist
	@rm -rf ${ENV} .env dist .pytest_cache
