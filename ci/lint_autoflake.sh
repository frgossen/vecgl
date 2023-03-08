#!/bin/bash

set -ex

python -m autoflake -r --check-diff example/*.py
python -m autoflake -r --check-diff src
python -m autoflake -r --check-diff test
