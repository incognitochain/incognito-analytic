import json

from service.pdex import PdexService


class PdexApi():
    def __init__(self, args):
        self.params = args

    def get(self):
        return "Pdex API"

    def getTokens(self):
        service = PdexService()
        data = service.getTokens()
        return data

    def getTradingPair(self):
        service = PdexService()
        data = service.getTradingPairs()
        return json.dumps(data)
