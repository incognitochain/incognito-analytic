#!/usr/bin/env bash
docker rm -f pdex-data-collector

docker rmi incognitochain/incognito-analytic:api-service

docker pull incognitochain/incognito-analytic:api-service

docker run --restart=always --net host -d -v $PWD/data:/data --name api-service incognitochain/incognito-analytic:api-service