.PHONY: help
.PHONY: dev
.PHONY: shell
.PHONY: seed
.PHONY: docs
.PHONY: tests
.PHONY: test
.PHONY: tox
.PHONY: hook
.PHONY: lint
.PHONY: migrate
.PHONY: migrations
.PHONY: mypy
.PHONY: Makefile

# Trick to allow passing commands to make
# Use quotes (" ") if command contains flags (-h / --help)
args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

# If command doesn't match, do not throw error
%:
	@:

define helptext

  Commands:

  dev                  Serve manual testing server
  shell                Run Django shell
  seed                 Run Django 'create_test_data' command
  docs                 Serve mkdocs for development.
  tests                Run all tests with coverage.
  test <name>          Run all tests maching the given <name>
  tox                  Run all tests with tox.
  hook                 Install pre-commit hook.
  lint                 Run pre-commit hooks on all files.
  migrate              Run pre-commit hooks on all files.
  migrations           Run pre-commit hooks on all files.
  mypy                 Run mypy on all files.

  Use quotes (" ") if command contains flags (-h / --help)
endef

export helptext

help:
	@echo "$$helptext"

dev:
	@poetry run python manage.py runserver 0.0.0.0:8000

shell:
	@poetry run python manage.py shell

seed:
	@poetry run python manage.py create_test_data

docs:
	@poetry run mkdocs serve -a localhost:8080

tests:
	@poetry run coverage run -m pytest

test:
	@poetry run pytest -k $(call args, "")

tox:
	@poetry run tox

hook:
	@poetry run pre-commit install

lint:
	@poetry run pre-commit run --all-files

migrate:
	@poetry run python manage.py migrate

migrations:
	@poetry run python manage.py makemigrations

mypy:
	@poetry run mypy graphene_django_extensions/
