#!/bin/bash

set -ex

python -m pytest test --benchmark-skip
