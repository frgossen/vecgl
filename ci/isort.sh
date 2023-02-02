#!/bin/bash

isort example/*.py --check-only
isort src --check-only
isort test --check-only
