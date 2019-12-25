# -*- coding: utf-8 -*-
from flask import Flask
from api.pdexapi import PdexApi
from api.tokenapi import TokenAPI
from api.transactionapi import TransactionAPI
from flask_restful import Resource, Api
from flask import request

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')


# PDEX Api
@app.route('/pdex', methods=['GET'])
def pdexApi():
    pdex = PdexApi(request.args)
    return pdex.get()


# DEX info
@app.route('/info', methods=['GET'])
def pdexInfo():
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
    pdex = PdexApi(request.args)
    return pdex.getMarketInfo()


# Get active trading pair
@app.route('/pdex/pairs', methods=['GET'])
@api.representation('application/json')
def pdexGetTradingPair():
    pdex = PdexApi(request.args)
    return pdex.getTradingPair()


# Get active trading token
@app.route('/pdex/tokens', methods=['GET'])
def pdexGetTradingToken():
    pdex = PdexApi(request.args)
    return pdex.getTokens()


# Count trading txs
@app.route('/pdex/count-trading-tx', methods=['GET'])
def pdexCountTradingTxs():
    pdex = PdexApi(request.args)
    return pdex.countTradingTxs()


# Last trading tx
# tokenSell=?
# tokenBuy=?
@app.route('/pdex/last-trading-tx', methods=['GET'])
def pdexGetLastTradingTx():
    pdex = PdexApi(request.args)
    return pdex.getLastTradingTx()


# Last volume 24 hours
# token1=?
# token2=?
# hours=24
@app.route('/pdex/last-volume', methods=['GET'])
def pdexLastVolume24Hours():
    pdex = PdexApi(request.args)
    return pdex.lastHoursVolume()


# Transaction API
@app.route('/transaction', methods=['GET'])
def transactionApi():
    transactionAPI = TransactionAPI(request.args)
    return transactionAPI.get()


# Get AVG Fee for token or PRV
# token_id=?
@app.route('/transaction/avg-fee', methods=['GET'])
def transactionGetAvgFee():
    transactionAPI = TransactionAPI(request.args)
    return transactionAPI.getAvgFee()


# List contribute liquidity tx
# page=
# limit=
# order_trend=
@app.route('/transaction/contribute-liquidity', methods=['GET'])
def listContributeLiquidityTxs():
    txApi = TransactionAPI(request.args)
    return txApi.listContributeLiquidityTx()


# List withdraw liquidity tx
# page=
# limit=
# order_trend=
@app.route('/transaction/withdraw-liquidity', methods=['GET'])
def listWithdrawLiquidityTxs():
    txApi = TransactionAPI(request.args)
    return txApi.listWithdrawLiquidityTx()


# List all token in network
@app.route('/token/list', methods=['GET'])
def getListTokens():
    tokenAPI = TokenAPI(request.args)
    return tokenAPI.listTokens()


# List all tx hash of token
# token_id=?
@app.route('/token/txs', methods=['GET'])
def getListTokenTxs():
    tokenAPI = TokenAPI(request.args)
    return tokenAPI.listTokenTxs()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
