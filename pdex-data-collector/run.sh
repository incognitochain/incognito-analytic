#!/usr/bin/env bash

mkdir -p /data

echo "run ./pdex-data-collector"
./pdex-data-collector > /data/log.txt 2>/data/error_log.txt