#!/bin/bash

set -ex

python -m autoflake -ir example/*.py
python -m autoflake -ir src
python -m autoflake -ir test

python -m isort example/*.py
python -m isort src
python -m isort test

python -m yapf -ir example/*.py
python -m yapf -ir src
python -m yapf -ir test
