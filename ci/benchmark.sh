#!/bin/bash

set -ex

python3 -m pytest test --benchmark-only --benchmark-save=$(date +%s)_$(git rev-parse HEAD)
