#!/bin/bash

set -ex

python -m pip install --upgrade pip
python -m pip install .[lint,test,release]
