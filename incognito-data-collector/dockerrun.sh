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

if [ -z "$postgresdb" ]; then
    postgresdb="pdex";
fi

docker run --restart=always --net host -d -v $PWD/data:/data -e postgreshost=$postgreshost -e postgresport=$postgresport -e postgresuser=$postgresuser -e postgrespwd=$postgrespwd -e postgresdb=$postgresdb --name incognito-data-collector incognitochain/incognito-analytic:incognito-data-collector