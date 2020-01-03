#!/bin/sh bash

run()
{
  validator_key=xxx
  bootnode="mainnet-bootnode.incognito.org:9330"
  is_shipping_logs=1
  latest_tag=$1
  current_tag=$2
  data_dir="data"
  eth_data_dir="eth-mainnet-data"
  eth_data_dir_geth="eth-mainnet-data-geth"
  logshipper_data_dir="logshipper-mainnet-data"

  docker -v || bash -c "wget -qO- https://get.docker.com/ | sh"

  if [ ! -d "$PWD/${eth_data_dir}" ]
  then
    mkdir $PWD/${eth_data_dir}
    chmod -R 777 $PWD/${eth_data_dir}
  fi

  if [ ! -d "$PWD/${eth_data_dir_geth}" ]
  then
    mkdir $PWD/${eth_data_dir_geth}
    chmod -R 777 $PWD/${eth_data_dir_geth}
  fi

  docker rm -f inc_mainnet
  docker rm -f eth_mainnet
  if [ "$current_tag" != "" ]
  then
    docker image rm -f incognitochain/incognito-mainnet:${current_tag}
  fi

  docker pull incognitochain/incognito-mainnet:${latest_tag}
  docker network create --driver bridge inc_net || true

  # docker rm -f eth_mainnet
  docker rm -f eth_mainnet

  # parity
  # docker run -ti --restart=always --net inc_net -d -p 8545:8545  -p 30303:30303 -p 30303:30303/udp -v $PWD/${eth_data_dir}:/home/parity/.local/share/io.parity.ethereum/ --name eth_mainnet  parity/parity:stable --light --jsonrpc-interface all --jsonrpc-hosts all  --jsonrpc-apis all --mode last --base-path=/home/parity/.local/share/io.parity.ethereum/

  # geth
  docker run --restart=always --net inc_net -d --name eth_mainnet -p 8545:8545 -p 30303:30303 -v $PWD/${eth_data_dir_geth}:/geth -it ethereum/client-go --syncmode light --datadir /geth --rpcaddr 0.0.0.0 --rpcport 8545 --rpc --rpccorsdomain "*"

  docker run --restart=always --net inc_net -p 9334:9334 -p 9433:9433 -e BOOTNODE_IP=$bootnode -e FULLNODE=1 -e GETH_NAME=eth_mainnet -e MININGKEY=${validator_key} -e TESTNET=false -v $PWD/${data_dir}:/data -d --name inc_mainnet incognitochain/incognito-mainnet:${latest_tag}

  if [ $is_shipping_logs -eq 1 ]
  then
    if [ ! -d "$PWD/${logshipper_data_dir}" ]
    then
      mkdir $PWD/${logshipper_data_dir}
      chmod -R 777 $PWD/${logshipper_data_dir}
    fi
    docker image rm -f incognitochain/logshipper:1.0.0
    docker run --restart=always -d --name inc_logshipper -e RAW_LOG_PATHS=/tmp/*.txt -e JSON_LOG_PATHS=/tmp/*.json -e LOGSTASH_ADDRESSES=34.94.14.147:5000 --mount type=bind,source=$PWD/${data_dir},target=/tmp --mount type=bind,source=$PWD/${logshipper_data_dir},target=/usr/share/filebeat/data incognitochain/logshipper:1.0.0
  fi
}

# kill existing run.sh processes
ps aux | grep '[i]ncognito-fullnode.sh' | awk '{ print $2}' | grep -v "^$$\$" | xargs kill -9

current_latest_tag=""
while [ 1 = 1 ]
do
  tags=`curl -X GET https://registry.hub.docker.com/v1/repositories/incognitochain/incognito-mainnet/tags  | sed -e 's/[][]//g' -e 's/"//g' -e 's/ //g' | tr '}' '\n'  | awk -F: '{print $3}' | sed -e 's/\n/;/g'`

  sorted_tags=($(echo ${tags[*]}| tr " " "\n" | sort -rn))
  latest_tag=${sorted_tags[0]}

  if [ "$current_latest_tag" != "$latest_tag" ]
  then
    run $latest_tag $current_latest_tag
    current_latest_tag=$latest_tag
  fi

  sleep 3600s

done &
