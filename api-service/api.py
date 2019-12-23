from flask import Flask
from api.pdexapi import PdexApi
from api.transactionapi import TransactionAPI
from flask_restful import Resource, Api
from flask import request

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')


@app.route('/pdex', methods=['GET'])
def pdexApi():
    pdex = PdexApi(request.args)
    return pdex.get()


@app.route('/pdex/pairs', methods=['GET'])
@api.representation('application/json')
def pdexGetTradingPair():
    pdex = PdexApi(request.args)
    return pdex.getTradingPair()


@app.route('/pdex/tokens', methods=['GET'])
def pdexGetTradingToken():
    pdex = PdexApi(request.args)
    return pdex.getTokens()


@app.route('/transaction', methods=['GET'])
def transactionApi():
    transactionAPI = TransactionAPI(request.args)
    return transactionAPI.get()


@app.route('/transaction/avg-fee', methods=['GET'])
def transactionGetAvgFee():
    transactionAPI = TransactionAPI(request.args)
    return transactionAPI.getAvgFee()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
