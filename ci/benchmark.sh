#!/bin/bash

set -ex

python -m pytest test --benchmark-only --benchmark-save=$(date +%s)_$(git rev-parse HEAD)
