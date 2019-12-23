#!/usr/bin/env bash

docker login

if [ -f ./pdex-data-collector ]; then
    rm -rf ./pdex-data-collector
fi

env CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags '-w' -o pdex-data-collector .

docker rmi incognitochain/incognito-analytic:pdex-data-collector
docker build . -t incognitochain/incognito-analytic:pdex-data-collector
docker push incognitochain/incognito-analytic:pdex-data-collector

if [ -f ./pdex-data-collector ]; then
    rm -rf ./pdex-data-collector
fi