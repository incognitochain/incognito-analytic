# -*- coding: utf-8 -*-
from flask import Flask
from api.pdexapi import PdexApi
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


# DEX info
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


# DEX market info
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


# Get active trading pair
@app.route('/pdex/pairs', methods=['GET'])
def pdexGetTradingPair():
    """
    Pdex Pairs
    ---
    tags:
        - Pdex API
    responses:
        200:
            description: Get active trading pair
    """
    pdex = PdexApi(request.args)
    return {'result': pdex.getTradingPair()}


# Get active trading token
@app.route('/pdex/tokens', methods=['GET'])
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
    return {'result': pdex.getTokens()}


# Count trading txs
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


# Last trading tx
# tokenSell=?
# tokenBuy=?
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


# Last volume 24 hours
# token1=?
# token2=?
# hours=24
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
    responses:
        200:
            description: Last trading tx
    """
    pdex = PdexApi(request.args)
    return {'result': pdex.lastHoursVolume()}


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


# Get AVG Fee for token or PRV
# token_id=?
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


# List contribute liquidity tx
# page=
# limit=
# order_trend=
# group=
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


# List withdraw liquidity tx
# page=
# limit=
# order_trend=
@app.route('/transaction/withdraw-liquidity', methods=['GET'])
def listWithdrawLiquidityTxs():
    txApi = TransactionAPI(request.args)
    return {'result': txApi.listWithdrawLiquidityTx()}


# List deposit centralized bridge token tx
# page=
# limit=
# order_trend=
@app.route('/transaction/deposit-centralized-bridge-token', methods=['GET'])
def listDepositCentralizedBridgeTokenTxs():
    txApi = TransactionAPI(request.args)
    return {'result': txApi.listDepositCentralizeBridgeTx()}


# List deposit decentralized bridge token tx
# page=
# limit=
# order_trend=
@app.route('/transaction/deposit-decentralized-bridge-token', methods=['GET'])
def listDepositDecentralizedBridgeTokenTxs():
    txApi = TransactionAPI(request.args)
    return {'result': txApi.listDepositDecentralizeBridgeTx()}


# List withdraw centralized bridge token tx
# page=
# limit=
# order_trend=
@app.route('/transaction/withdraw-centralized-bridge-token', methods=['GET'])
def listWithdrawCentralizedBridgeTokenTxs():
    txApi = TransactionAPI(request.args)
    return {'result': txApi.listWithdrawCentralizeBridgeTx()}


# List withdraw decentralized bridge token tx
# page=
# limit=
# order_trend=
@app.route('/transaction/withdraw-decentralized-bridge-token', methods=['GET'])
def listWithdrawDecentralizedBridgeTokenTxs():
    txApi = TransactionAPI(request.args)
    return {'result': txApi.listWithdrawDecentralizeBridgeTx()}


# List all token in network
@app.route('/token/list', methods=['GET'])
def getListTokens():
    tokenAPI = TokenAPI(request.args)
    return {'result': tokenAPI.listTokens()}


# List all tx hash of token
# token_id=?
@app.route('/token/txs', methods=['GET'])
def getListTokenTxs():
    tokenAPI = TokenAPI(request.args)
    return {'result': tokenAPI.listTokenTxs()}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
