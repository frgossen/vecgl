#!/bin/bash

set -ex

# Release only if this commit is tagged with a version of the form `v.0.0.1`.
HAS_VERSION_TAG=0
for TAG in $(git tag --points-at HEAD); do
  if [[ $TAG =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    HAS_VERSION_TAG=1
  fi
done
if [[ $HAS_VERSION_TAG == 0 ]]; then
  exit 0
fi

# Upload to PyPI
python -m twine check dist/*
python -m twine upload dist/* -u=__token__ -p=$PYPI_API_TOKEN
