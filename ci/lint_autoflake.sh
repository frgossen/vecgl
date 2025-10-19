#!/bin/bash

set -ex

python3 -m autoflake -r --check-diff example/*.py
python3 -m autoflake -r --check-diff src
python3 -m autoflake -r --check-diff test
