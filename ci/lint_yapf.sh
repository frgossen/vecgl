#!/bin/bash

set -ex

python -m yapf -qr example/*.py
python -m yapf -qr src
python -m yapf -qr test
