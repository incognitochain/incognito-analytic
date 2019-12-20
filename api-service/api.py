from flask import Flask
from api.pdex import Pdex, PdexTradingPair, PdexToken
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')
api.add_resource(Pdex, '/pdex')
api.add_resource(PdexTradingPair, '/pdex/pairs')
api.add_resource(PdexToken, '/pdex/tokens')

if __name__ == '__main__':
    app.run(debug=True)
