#!/usr/bin/env bash

docker rm -f incognito-data-collector

docker rmi incognitochain/incognito-analytic:incognito-data-collector

docker pull incognitochain/incognito-analytic:incognito-data-collector

docker run --restart=always --net host -d -v $PWD/data:/data --name incognito-data-collector incognitochain/incognito-analytic:incognito-data-collector