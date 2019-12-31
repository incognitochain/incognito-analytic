# -*- coding: utf-8 -*-
from flask import Flask

from api.blockapi import BlockAPI
from api.pdexapi import PdexApi
from api.stakeapi import StakeAPI
from api.tokenapi import TokenAPI
from api.transactionapi import TransactionAPI
from flask import request
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)


# PDEX Api
@app.route('/pdex', methods=['GET'])
def pdexApi():
    """
    Pdex Default
    ---
    tags:
      - Pdex API
    """
    pdex = PdexApi(request.args)
    return {'result': pdex.get()}


@app.route('/info', methods=['GET'])
def pdexInfo():
    """
    Pdex Info
    ---
    tags:
      - Pdex API
    responses:
        200:
            description: Get pDex info
    """
    result = {
        "name": "Incognito Privacy Decentralized Exchange",
        "description": """Completely anonymous trading – no KYC, no records of buyers, sellers or transaction amounts. No third party risk – you control your money and hold your own private keys. Decentralized, scalable, cross-chain liquidity. Trade BTC, ETH, PRV and more with 100% confidentiality.""",
        "location": "Vietnam",
        "logo": "https://incognito.org/assets/236ce48.svg",
        "website": "https://incognito.org/",
        "twitter": "Incognito Chain",
        "version": "1.0",
        "capability": {
            "markets": True,
            "trades": True,
            "ordersSnapshot": False,
            "candles": False,
            "ticker": False
        }
    }
    return result


@app.route("/market")
def pdexMarket():
    """
        Pdex Market
        ---
        tags:
            - Pdex API
        responses:
            200:
                description: Get pDex market
        """
    pdex = PdexApi(request.args)
    return pdex.getMarketInfo()


@app.route('/pdex/pairs', methods=['GET'])
def pdexGetTradingPair():
    """
    Pdex Pairs
    ---
    tags:
        - Pdex API
    responses:
        200:
            description: Get active trading pair. Update list pairs
    """
    pdex = PdexApi(request.args)
    return {'result': pdex.getTradingPair()}


@app.route('/pdex/tokens', methods=['GET', 'PUT'])
def pdexGetTradingToken():
    """
    Pdex Pairs Token
    ---
    tags:
        - Pdex API
    responses:
        200:
            description: Get active trading token
    """
    pdex = PdexApi(request.args)
    if request.method == 'GET':
        return {'result': pdex.getTokens()}
    elif request.method == 'PUT':
        return {'result': pdex.updateListTokens()}


@app.route('/pdex/count-trading-tx', methods=['GET'])
def pdexCountTradingTxs():
    """
    Pdex trading txs
    ---
    tags:
        - Pdex API
    responses:
        200:
            description: Count trading txs
    """
    pdex = PdexApi(request.args)
    return {'result': pdex.countTradingTxs()}


@app.route('/pdex/last-trading-tx', methods=['GET'])
def pdexGetLastTradingTx():
    """
    Pdex last trading tx
    ---
    tags:
        - Pdex API
    parameters:
      - name: tokenSell
        in: query
        type: string
        required: true
      - name: tokenBuy
        in: query
        type: string
        required: true
    responses:
        200:
            description: Last trading tx
    """
    pdex = PdexApi(request.args)
    return {'result': pdex.getLastTradingTx()}


@app.route('/pdex/last-volume', methods=['GET'])
def pdexLastVolume24Hours():
    """
    Pdex last trading tx
    ---
    tags:
        - Pdex API
    parameters:
      - name: token1
        in: query
        type: string
        required: true
      - name: token2
        in: query
        type: string
        required: true
      - name: hours
        in: query
        type: string
        required: true
      - name: direction
        in: query
        type: string
        required: false
        default: false
    responses:
        200:
            description: Last trading tx
    """
    pdex = PdexApi(request.args)
    return {'result': pdex.lastHoursVolume()}


@app.route('/pdex/trader/leader-board/by-count-trade-tx', methods=['GET'])
def leaderTraderByTradeTxs():
    """
    Leader board by number of trading tx
    ---
    parameters:
        - name: hours
          in: query
          type: string
          required: false
          default: 24
    tags:
        - Pdex API
    responses:
        200:
            description: Leader board by number of trading tx
    """
    pdex = PdexApi(request.args)
    return {'result': pdex.leaderTraderByTradeTxs()}


@app.route('/pdex/trader/leader-board/by-count-volume', methods=['GET'])
def leaderTraderByVolume():
    """
    Leader board by number of trading tx
    ---
    parameters:
        - name: token1
          in: query
          type: string
          required: true
        - name: token2
          in: query
          type: string
          required: true
        - name: hours
          in: query
          type: string
          required: false
          default: 24
    tags:
        - Pdex API
    responses:
        200:
            description: Leader board by number of trading tx
    """
    pdex = PdexApi(request.args)
    return {'result': pdex.leaderTraderByVolume()}


# Transaction API
@app.route('/transaction', methods=['GET'])
def transactionApi():
    """
    Transaction API
    ---
    tags:
        - Transaction API
    responses:
        200:
            description: Transaction API
    """
    transactionAPI = TransactionAPI(request.args)
    return {'result': transactionAPI.get()}


@app.route('/transaction/count', methods=['GET'])
def countTotaTx():
    """
    Count total tx
    ---
    tags:
        - Transaction API
    responses:
        200:
            description: Count total tx
    """
    transactionAPI = TransactionAPI(request.args)
    return {'result': transactionAPI.countTx()}


@app.route('/transaction/detail', methods=['GET'])
def getTxByHash():
    """
    Get tx by hash
    ---
    tags:
        - Transaction API
    parameters:
        - name: hash
          type: string
          in: query
          required: true
    responses:
        200:
            description: Get tx by hash
    """
    transactionAPI = TransactionAPI(request.args)
    return {'result': transactionAPI.getTxByHash()}


@app.route('/transaction/avg-fee', methods=['GET'])
def transactionGetAvgFee():
    """
    Get AVG Fee for token or PRV
    ---
    tags:
        - Transaction API
    parameters:
        - name: token_id
          in: query
          type: string
          required: false

    responses:
        200:
            description: Get AVG Fee for Token or PRV
    """
    transactionAPI = TransactionAPI(request.args)
    return {'result': transactionAPI.getAvgFee()}


@app.route('/transaction/contribute-liquidity', methods=['GET'])
def listContributeLiquidityTxs():
    """
    List contribute liquidity tx
    ---
    tags:
        - Transaction API
    parameters:
        - name: page
          in: query
          type: string
          required: false
          default: 0
        - name: limit
          in: query
          type: string
          required: false
          default: 0
        - name: order_trend
          in: query
          type: string
          required: false
          default: asc
        - name: group
          in: query
          type: string
          required: false
          default: 0

    responses:
        200:
            description: List contribute liquidity tx
    """
    txApi = TransactionAPI(request.args)
    return {'result': txApi.listContributeLiquidityTx()}


@app.route('/transaction/withdraw-liquidity', methods=['GET'])
def listWithdrawLiquidityTxs():
    """
    List withdraw liquidity tx
    ---
    tags:
        - Transaction API
    parameters:
        - name: page
          in: query
          type: string
          required: false
          default: 0
        - name: limit
          in: query
          type: string
          required: false
          default: 0
        - name: order_trend
          in: query
          type: string
          required: false
          default: asc

    responses:
        200:
            description: List withdraw liquidity tx
    """
    txApi = TransactionAPI(request.args)
    return {'result': txApi.listWithdrawLiquidityTx()}


@app.route('/transaction/deposit-centralized-bridge-token', methods=['GET'])
def listDepositCentralizedBridgeTokenTxs():
    """
    List deposit centralized bridge token tx
    ---
    tags:
        - Transaction API
    parameters:
        - name: page
          in: query
          type: string
          required: false
          default: 0
        - name: limit
          in: query
          type: string
          required: false
          default: 0
        - name: order_trend
          in: query
          type: string
          required: false
          default: asc

    responses:
        200:
            description: List deposit centralized bridge token tx
    """
    txApi = TransactionAPI(request.args)
    return {'result': txApi.listDepositCentralizeBridgeTx()}


@app.route('/transaction/deposit-decentralized-bridge-token', methods=['GET'])
def listDepositDecentralizedBridgeTokenTxs():
    """
    List deposit decentralized bridge token tx
    ---
    tags:
        - Transaction API
    parameters:
        - name: page
          in: query
          type: string
          required: false
          default: 0
        - name: limit
          in: query
          type: string
          required: false
          default: 0
        - name: order_trend
          in: query
          type: string
          required: false
          default: asc

    responses:
        200:
            description: List deposit decentralized bridge token tx
    """
    txApi = TransactionAPI(request.args)
    return {'result': txApi.listDepositDecentralizeBridgeTx()}


@app.route('/transaction/withdraw-centralized-bridge-token', methods=['GET'])
def listWithdrawCentralizedBridgeTokenTxs():
    """
    List withdraw centralized bridge token tx
    ---
    tags:
        - Transaction API
    parameters:
        - name: page
          in: query
          type: string
          required: false
          default: 0
        - name: limit
          in: query
          type: string
          required: false
          default: 0
        - name: order_trend
          in: query
          type: string
          required: false
          default: asc

    responses:
        200:
            description: List withdraw centralized bridge token tx
    """
    txApi = TransactionAPI(request.args)
    return {'result': txApi.listWithdrawCentralizeBridgeTx()}


@app.route('/transaction/withdraw-decentralized-bridge-token', methods=['GET'])
def listWithdrawDecentralizedBridgeTokenTxs():
    """
    List withdraw decentralized bridge token tx
    ---
    tags:
        - Transaction API
    parameters:
        - name: page
          in: query
          type: string
          required: false
          default: 0
        - name: limit
          in: query
          type: string
          required: false
          default: 0
        - name: order_trend
          in: query
          type: string
          required: false
          default: asc

    responses:
        200:
            description: List withdraw centralized bridge token tx
    """
    txApi = TransactionAPI(request.args)
    return {'result': txApi.listWithdrawDecentralizeBridgeTx()}


@app.route('/token/list', methods=['GET'])
def getListTokens():
    """
    List all token in network
    ---
    tags:
        - Token API
    responses:
        200:
            description: List all token in network
    """
    tokenAPI = TokenAPI(request.args)
    return {'result': tokenAPI.listTokens()}


@app.route('/token/txs', methods=['GET'])
def getListTokenTxs():
    """
    List all tx hash of token
    ---
    tags:
        - Token API
    parameters:
        - name: token_id
          type: string
          in: query
          required: true
    responses:
        200:
            description: List all tx hash of token
    """
    tokenAPI = TokenAPI(request.args)
    return {'result': tokenAPI.listTokenTxs()}


# Bock API
@app.route('/block/beacon/count', methods=['GET'])
def countBeaconBlock():
    """
    Count beacon block
    ---
    tags:
        - Beacon Block API
    responses:
        200:
            description: Count beacon block
    """
    blockAPI = BlockAPI(request.args)
    return {
        'result': blockAPI.countBeaconBlock()
    }


@app.route('/block/beacon/last-block', methods=['GET'])
def lastBeaconBlock():
    """
    Last beacon block
    ---
    tags:
        - Beacon Block API
    responses:
        200:
            description: Last beacon block
    """
    blockAPI = BlockAPI(request.args)
    return {
        'result': blockAPI.lastBeaconBlock()
    }


@app.route('/block/beacon/list', methods=['GET'])
def listBeaconBlock():
    """
    List beacon block
    ---
    tags:
        - Beacon Block API
    parameters:
        - name: page
          type: string
          in: query
          default: 0
          required: true
        - name: limit
          type: string
          in: query
          default: 0
          required: true
    responses:
        200:
            description: List beacon block
    """
    blockAPI = BlockAPI(request.args)
    return {
        'result': blockAPI.listBeaconBlock()
    }


@app.route('/block/beacon/block', methods=['GET'])
def getBeaconBlock():
    """
    Get beacon block
    ---
    tags:
        - Beacon Block API
    parameters:
        - name: block_height
          type: string
          in: query
          default: 0
          required: false
        - name: block_hash
          type: string
          in: query
          default: 0
          required: false
    responses:
        200:
            description: Get beacon block
    """
    blockAPI = BlockAPI(request.args)
    return {
        'result': blockAPI.getBeaconBlock()
    }


@app.route('/block/shard/count', methods=['GET'])
def countShardBlock():
    """
    Count shard block
    ---
    tags:
        - Shard Block API
    parameters:
        - name: shard_id
          type: string
          in: query
          default: 0
          required: true
    responses:
        200:
            description: Count shard block
    """
    blockAPI = BlockAPI(request.args)
    return {
        'result': blockAPI.countShardBlock()
    }


@app.route('/block/shard/last-block', methods=['GET'])
def lastShardBlock():
    """
    Last shard block
    ---
    tags:
        - Shard Block API
    responses:
        200:
            description: Last shard block
    """
    blockAPI = BlockAPI(request.args)
    return {
        'result': blockAPI.lastShardBlock()
    }


@app.route('/block/shard/list', methods=['GET'])
def listShardBlock():
    """
    List shard block
    ---
    tags:
        - Shard Block API
    parameters:
        - name: shard_id
          type: string
          in: query
          default: 0
          required: true
        - name: page
          type: string
          in: query
          default: 0
          required: true
        - name: limit
          type: string
          in: query
          default: 0
          required: true
    responses:
        200:
            description: List shard block
    """
    blockAPI = BlockAPI(request.args)
    return {
        'result': blockAPI.listShardBlock()
    }


@app.route('/block/shard/block', methods=['GET'])
def getShardBlock():
    """
    Get shard block
    ---
    tags:
        - Shard Block API
    parameters:
        - name: block_height
          type: string
          in: query
          default: 0
          required: false
        - name: block_hash
          type: string
          in: query
          default: 0
          required: false
    responses:
        200:
            description: Get shard block
    """
    blockAPI = BlockAPI(request.args)
    return {
        'result': blockAPI.getShardBlock()
    }


# Stake
@app.route('/stake/minded-token', methods=['GET'])
def mindedToken():
    """
    Get mined PRV token
    ---
    tags:
        - Stake API
    responses:
        200:
            description: Get mined PRV token
    """
    stakeAPI = StakeAPI(request.args)
    return {
        'result': stakeAPI.getMinedPRVToken(),
    }


@app.route('/stake/staked-token', methods=['GET'])
def stakedToken():
    """
    Get total staked PRV token
    ---
    tags:
        - Stake API
    responses:
        200:
            description: Get total staked PRV token
    """
    stakeAPI = StakeAPI(request.args)
    return {
        'result': stakeAPI.getTotalStakedTokens(),
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
