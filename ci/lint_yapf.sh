#!/bin/bash

set -ex

python -m yapf -r --diff example/*.py
python -m yapf -r --diff src
python -m yapf -r --diff test
