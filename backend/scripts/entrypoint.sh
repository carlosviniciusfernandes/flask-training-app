#! /bin/bash

cd /backend
poetry install --no-root


cd /backend/src
poetry run python main.py
