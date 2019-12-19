#!/usr/bin/env bash

mkdir data

docker rm -f pdex-data-collector

docker run --restart=always -d -v $PWD/data:/data --name pdex-data-collector incognitochain/incognito-analytic:pdex-data-collector