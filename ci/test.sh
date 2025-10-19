#!/bin/bash

set -ex

python3 -m pytest test --benchmark-skip
