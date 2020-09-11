#!/usr/bin/env bash
docker rm -f incognito-analytic-api-service

docker rmi incognitochain/incognito-analytic:incognito-analytic-api-service

docker pull incognitochain/incognito-analytic:incognito-analytic-api-service

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

if [ -z "$redishost" ]; then
    redishost="127.0.0.1";
fi

docker run --restart=always -p 8080:5000 -d -v $PWD/data:/data -e redishost=$redishost -e postgreshost=$postgreshost -e postgresport=$postgresport -e postgresuser=$postgresuser -e postgrespwd=$postgrespwd -e postgresdb=$postgresdb --name incognito-analytic-api-service incognitochain/incognito-analytic:incognito-analytic-api-service