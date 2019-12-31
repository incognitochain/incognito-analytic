#!/usr/bin/env bash

mkdir -p /data

echo "pip install -r /app/requirements.txt"
pip install -r /app/requirements.txt > /data/install_python_lib.txt

echo "python api.py > /data/log_api_service.txt 2>/data/error_log_api_service.txt"
python api.py > /data/log_api_service.txt 2>/data/error_log_api_service.txt