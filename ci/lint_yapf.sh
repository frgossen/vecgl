#!/bin/bash

set -ex

python3 -m yapf -r --diff example/*.py
python3 -m yapf -r --diff src
python3 -m yapf -r --diff test
