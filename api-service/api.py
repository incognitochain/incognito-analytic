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
# token1=?
# token2=?
@app.route('/pdex/last-trading-tx', methods=['GET'])
def pdexGetLastTradingTx():
    pdex = PdexApi(request.args)
    return pdex.getLastTradingTx()


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
