#!/bin/bash

set -e

python -m pytest test --benchmark-skip
