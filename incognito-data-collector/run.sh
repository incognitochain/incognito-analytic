#!/usr/bin/env bash

mkdir -p /data

if [ -z "$postgrespwd" ]; then
    postgrespwd="postgres";
fi

if [ -z "$postgresuser" ]; then
    postgresuser="postgres";
fi

if [ -z "$postgreshost" ]; then
    postgreshost="127.0.0.1";
fi

if [ -z "$postgresport" ]; then
    postgresport="5432";
fi

echo "run ./incognito-data-collector"
./incognito-data-collector postgreshost=$postgreshost postgresport=$postgresport postgresuser=$postgresuser postgrespwd=$postgrespwd  > /data/log.txt 2>/data/error_log.txt