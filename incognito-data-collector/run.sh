#!/usr/bin/env bash

mkdir -p /data

echo "run ./incognito-data-collector"
./incognito-data-collector > /data/log.txt 2>/data/error_log.txt