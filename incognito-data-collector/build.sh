#!/usr/bin/env bash

docker login

if [ -f ./incognito-data-collector ]; then
    rm -rf ./incognito-data-collector
fi

env CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags '-w' -o incognito-data-collector .

docker rmi incognitochain/incognito-analytic:incognito-data-collector
docker build . -t incognitochain/incognito-analytic:incognito-data-collector
docker push incognitochain/incognito-analytic:incognito-data-collector

if [ -f ./incognito-data-collector ]; then
    rm -rf ./incognito-data-collector
fi