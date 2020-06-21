#!/usr/bin/env bash
set -eo pipefail

# Installation
rm -rf .venv package layer.zip lambda_package.zip
virtualenv -p `which python3` .venv
source .venv/bin/activate
rm -rf package
cd src
pip install --target ../package/python -r requirements.txt

# Build layer
cd ../package
zip -r ../layer.zip .
cd ..

# Build lambda package
cd src
zip -r ../lambda_package.zip main.py