#!/bin/bash

set -ex

python3 -m ensurepip --upgrade
python3 -m pip install --editable .[lint,test,release]
