.PHONY: test help clean clean-pyc clean-venv lint tox
.DEFAULT: test

help:
	@echo "Usage:"
	@echo "venv"
	@echo "		Create virtualenv if needed."
	@echo "install-dev"
	@echo "		Install 'dev' requirements."
	@echo "test"
	@echo "		Run pytest"
	@echo "clean"
	@echo "		Clean stuff."

PROJECT = qson
ifeq (${VIRTUAL_ENV},)
  VENV_NAME = .venv
  CLEAN_VENV = rm -rf ${VENV_NAME}
else
  VENV_NAME = ${VIRTUAL_ENV}
  CLEAN_VENV = @echo "Can't delete activated virtualenv '${VENV_NAME}'"
endif
${info Using ${VENV_NAME}}

VENV_BIN = ${VENV_NAME}/bin
ifeq (${VIRTUAL_ENV},)
  VENV_ACTIVATE = . ${VENV_BIN}/activate
else
  VENV_ACTIVATE = true
endif
PYTHON = ${VENV_BIN}/python

venv: ${VENV_NAME}/venv-created
${VENV_NAME}/venv-created:
	test -d ${VENV_NAME} || python -m venv ${VENV_NAME}
	@touch $@

install-dev: venv ${VENV_NAME}/dev.installed
${VENV_NAME}/dev.installed: setup.py setup.cfg requirements.txt
	${VENV_ACTIVATE}; pip install -e .[dev]
	@touch $@

test: install-dev clean-pyc
	${VENV_ACTIVATE}; pytest --cov=${PROJECT} --cov-report=term-missing tests

tox:
	tox

lint:
	black ${PROJECT}
	isort -rc ${PROJECT}
	flake8 ${PROJECT} tests

clean: clean-pyc clean-venv

clean-pyc:
	find . -name '*.pyc' -exec rm {} \;

clean-venv:
	${CLEAN_VENV}
