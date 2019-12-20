from flask_restful import Resource
from service.pdex import PdexService


class Pdex(Resource):
    def get(self):
        return "Pdex API"


class PdexToken(Resource):
    def get(self):
        service = PdexService()
        data = service.getToken()
        return data


class PdexTradingPair(Resource):
    def get(self):
        service = PdexService()
        data = service.getTradingPairs()
        return data
