#!/bin/bash

set -ex

python -m isort example/*.py
python -m isort src
python -m isort test
