#!/bin/bash

set -ex

python -m isort example/*.py --check-only
python -m isort src --check-only
python -m isort test --check-only
