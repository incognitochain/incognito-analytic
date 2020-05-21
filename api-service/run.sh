#!/usr/bin/env bash

mkdir -p /data

echo "pip install -r /app/requirements.txt"
pip install -r /app/requirements.txt > /data/install_python_lib.txt

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

if [ -z "$postgresdb" ]; then
    postgresdb="pdex";
fi

echo "python api.py > /data/log_api_service.txt 2>/data/error_log_api_service.txt"
postgreshost=$postgreshost postgresport=$postgresport postgresuser=$postgresuser postgrespwd=$postgrespwd postgresdb=$postgresdb python api.py > /data/log_api_service.txt 2>/data/error_log_api_service.txt

#echo "python cronjobs/cronjob.py"
#Webhookvivian=$Webhookvivian python cronjobs/cronjob.py > /data/notify_service.txt 2> /data/err_notify_service.txt