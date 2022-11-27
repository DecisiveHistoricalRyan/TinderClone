#!/bin/sh -e
set -x

isort --line-length 120 .
black --line-length 120 .
flake8 --max-line-length 120 .
mypy --check-untyped-defs -p app

