#!/usr/bin/env bash

docker rm -f incognito-data-collector

docker rmi incognitochain/incognito-analytic:incognito-data-collector

docker pull incognitochain/incognito-analytic:incognito-data-collector

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

docker run --restart=always --net host -d -v $PWD/data:/data  -e postgrespwd=$postgrespwd --name incognito-data-collector incognitochain/incognito-analytic:incognito-data-collector