#!/usr/bin/env bash

docker login

docker rmi incognitochain/incognito-analytic:api-service
docker build . -t incognitochain/incognito-analytic:api-service
docker push incognitochain/incognito-analytic:api-service