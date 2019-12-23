#!/usr/bin/env bash
docker rm -f incognito-analytic-api-service

docker rmi incognitochain/incognito-analytic:incognito-analytic-api-service

docker pull incognitochain/incognito-analytic:incognito-analytic-api-service

docker run --restart=always -p 8080:5000 -d -v $PWD/data:/data --name incognito-analytic-api-service incognitochain/incognito-analytic:incognito-analytic-api-service