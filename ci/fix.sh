#!/bin/bash

set -ex

python3 -m autoflake -ir example/*.py
python3 -m autoflake -ir src
python3 -m autoflake -ir test

python3 -m isort example/*.py
python3 -m isort src
python3 -m isort test

python3 -m yapf -ir example/*.py
python3 -m yapf -ir src
python3 -m yapf -ir test
