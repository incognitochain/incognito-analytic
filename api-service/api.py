from flask import Flask
from api.pdex import Pdex, PdexTradingPair, PdexToken
from api.transactionapi import TransactionAPI
from flask_restful import Resource, Api
from flask import request

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')
api.add_resource(Pdex, '/pdex')
api.add_resource(PdexTradingPair, '/pdex/pairs')
api.add_resource(PdexToken, '/pdex/tokens')


@app.route('/transaction/avg-fee', methods=['GET'])
def getAvgFee():
    transactionAPI = TransactionAPI(request.args)
    return transactionAPI.getAvgFee()


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
