# -*- coding: utf-8 -*-
import json
from flask_restful import fields, marshal

from service.pdex import PdexService
from service.token import TokenService


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

    def countTradingTxs(self):
        service = PdexService()
        count = service.countTradingTxs()
        return {'count': count}

    def getLastTradingTx(self):
        service = PdexService()
        tokenSell = self.params.get("tokenSell", "")
        tokenBuy = self.params.get("tokenBuy", "")
        data = service.lastTradingTx(tokenSell, tokenBuy)
        return data

    def getMarketInfo(self):
        result = []
        service = PdexService()
        tradingPairs = service.getTradingPairs()
        for pair in tradingPairs:
            keys = list(pair.keys())
            token1 = pair[keys[0]]
            token2 = pair[keys[1]]

            item = {
                "id": token1["name"] + "_" + token2["name"],
                "type": "spot",
                "base": token1["name"],
                "quote": token2["name"],
                "active": True,
                # "subtypes": [],
                # "settlement": "USDT",
                # "market_url": "https://www.binance.com/en/futures/BTCUSDT",
                # "description": "Binance perpetual futures market for BTC quoted in USDT"
            }

            result.append(item)

        # result = [
        #     {
        #         "id": "ETH_BTC",
        #         "type": "spot",
        #         "base": "ETH",
        #         "quote": "BTC"
        #     },
        #     {
        #         "id": "BTC_USDT",
        #         "type": "derivative",
        #         "base": "BTC",
        #         "quote": "USDT",
        #         "active": True,
        #         "subtypes": ["perpetual", "future"],
        #         "settlement": "USDT",
        #         "market_url": "https://www.binance.com/en/futures/BTCUSDT",
        #         "description": "Binance perpetual futures market for BTC quoted in USDT"
        #     },
        #     {
        #         "id": "in_xrpxbt",
        #         "type": "index",
        #         "base": "XRP",
        #         "quote": "XBT",
        #         "active": True,
        #         "market_url": "https://www.cfbenchmarks.com/indices/XRP/XBT/RTI/seconds"
        #     }
        # ]
        return json.dumps(result)

    def lastHoursVolume(self):
        token1 = self.params.get('token1', '')
        token2 = self.params.get('token2', '')
        # default 24 hours
        hours = self.params.get('hours', 24)

        if token1 == '' and token2 == '':
            return {}
        else:
            service = PdexService()
            tokenService = TokenService()

            data = service.lastTradingTxInHours(token1, token2, hours)
            if len(data) == 0:
                return {}

            result = {}
            tokens = tokenService.listTokens()
            for tx in data:
                metadata = tx['metadata']
                if metadata['TokenIDToSellStr'] == '0000000000000000000000000000000000000000000000000000000000000004':
                    sellToken = 'PRV'
                else:
                    sellToken = tokens[metadata['TokenIDToSellStr']]['name']
                sellAmount = metadata['SellAmount']
                if metadata['TokenIDToBuyStr'] == '0000000000000000000000000000000000000000000000000000000000000004':
                    buyToken = 'PRV'
                else:
                    buyToken = tokens[metadata['TokenIDToBuyStr']]['name']
                buyAmount = tx['receive_amount']

                if sellToken not in result:
                    result[sellToken] = 0
                result[sellToken] += sellAmount

                if buyToken not in result:
                    result[buyToken] = 0
                result[buyToken] += buyAmount
            return result
