#!/usr/bin/env bash
set -eo pipefail

virtualenv -p `which python3` .venv
source .venv/bin/activate
rm -rf package
cd src
pip install --target ../package/python -r requirements.txt
cd ../package
zip -r ../layer.zip .