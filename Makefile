include .env
EXPORT = export PYTHONPATH=$(PWD)

checks:
	$(EXPORT) && pipenv run sh scripts/checks.sh