#!/bin/bash

set -ex

python3 -m isort example/*.py --check-only
python3 -m isort src --check-only
python3 -m isort test --check-only
