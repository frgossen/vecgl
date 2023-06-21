#!/bin/bash

set -ex

python -m ensurepip --upgrade
python -m pip install --editable .[lint,test,release]
