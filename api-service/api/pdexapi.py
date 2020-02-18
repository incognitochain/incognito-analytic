# -*- coding: utf-8 -*-
import json

import requests
from operator import itemgetter
from service.pdexservice import PdexService
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
        return data

    def countTradingTxs(self):
        service = PdexService()
        count = service.countTradingTxs()
        return {'count': count}

    def getLastTradingTx(self):
        tokenSell = self.params.get("tokenSell", "")
        tokenBuy = self.params.get("tokenBuy", "")
        return self.getLastTradingTxFunc(tokenSell, tokenBuy)

    def getLastTradingTxFunc(self, tokenSell, tokenBuy):
        service = PdexService()
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
                "id": token1["id"] + "_" + token2["id"],
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
        return result

    def commonPairsLatest24Hours(self):
        tradeTokens = self.getTokens()

        commonPairs = {
            'pZRX-PRV': {
                'tokenBuy': 'de395b1914718702687b477703bdd36e52119033a9037bb28f6b33a3d0c2f867',
                'tokenSell': '0000000000000000000000000000000000000000000000000000000000000004',
            },
            'pLINK-PRV': {
                'tokenBuy': 'e0926da2436adc42e65ca174e590c7b17040cd0b7bdf35982f0dd7fc067f6bcf',
                'tokenSell': '0000000000000000000000000000000000000000000000000000000000000004',
            },
            'pTOMO-pUSDT': {
                'tokenBuy': 'a0a22d131bbfdc892938542f0dbe1a7f2f48e16bc46bf1c5404319335dc1f0df',
                'tokenSell': '716fd1009e2a1669caacc36891e707bfdf02590f96ebd897548e8963c95ebac0',
            },
            'pTOMO-PRV': {
                'tokenBuy': 'a0a22d131bbfdc892938542f0dbe1a7f2f48e16bc46bf1c5404319335dc1f0df',
                'tokenSell': '0000000000000000000000000000000000000000000000000000000000000004',
            },
            'pBAND-PRV': {
                'tokenBuy': '2dda855fb4660225882d11136a64ad80effbddfa18a168f78924629b8664a6b3',
                'tokenSell': '0000000000000000000000000000000000000000000000000000000000000004',
            },
            'pFTM-pUSDT': {
                'tokenBuy': 'd09ad0af0a34ea3e13b772ef9918b71793a18c79b2b75aec42c53b69537029fe',
                'tokenSell': '716fd1009e2a1669caacc36891e707bfdf02590f96ebd897548e8963c95ebac0',
            },
            'pZIL-PRV': {
                'tokenBuy': '880ea0787f6c1555e59e3958a595086b7802fc7a38276bcd80d4525606557fbc',
                'tokenSell': '0000000000000000000000000000000000000000000000000000000000000004',
            },
            'pMATIC-PRV': {
                'tokenBuy': 'dae027b21d8d57114da11209dce8eeb587d01adf59d4fc356a8be5eedc146859',
                'tokenSell': '0000000000000000000000000000000000000000000000000000000000000004',
            },
            'pONE-PRV': {
                'tokenBuy': '4077654cf585a99b448564d1ecc915baf7b8ac58693d9f0a6af6c12b18143044',
                'tokenSell': '0000000000000000000000000000000000000000000000000000000000000004',
            },
            'pONE-pUSDT': {
                'tokenBuy': '4077654cf585a99b448564d1ecc915baf7b8ac58693d9f0a6af6c12b18143044',
                'tokenSell': '716fd1009e2a1669caacc36891e707bfdf02590f96ebd897548e8963c95ebac0',
            },
            'pBAT-PRV': {
                'tokenBuy': '1fe75e9afa01b85126370a1583c7af9f1a5731625ef076ece396fcc6584c2b44',
                'tokenSell': '0000000000000000000000000000000000000000000000000000000000000004',
            },
            'pBNB-PRV': {
                'tokenBuy': 'b2655152784e8639fa19521a7035f331eea1f1e911b2f3200a507ebb4554387b',
                'tokenSell': '0000000000000000000000000000000000000000000000000000000000000004',
            },
            'pWTC-PRV': {
                'tokenBuy': '530cd74f506edcdd263e34e6dacdd15097f87677036cf412f8ebeb1c494e352d',
                'tokenSell': '0000000000000000000000000000000000000000000000000000000000000004',
            },
            'PRV-pBTC': {
                'tokenBuy': '0000000000000000000000000000000000000000000000000000000000000004',
                'tokenSell': 'b832e5d3b1f01a4f0623f7fe91d6673461e1f5d37d91fe78c5c2e6183ff39696',
            },
            'pBTC-pUSDT': {
                'tokenBuy': 'b832e5d3b1f01a4f0623f7fe91d6673461e1f5d37d91fe78c5c2e6183ff39696',
                'tokenSell': '716fd1009e2a1669caacc36891e707bfdf02590f96ebd897548e8963c95ebac0',
            },
            'PRV-pETH': {
                'tokenBuy': '0000000000000000000000000000000000000000000000000000000000000004',
                'tokenSell': 'ffd8d42dc40a8d166ea4848baf8b5f6e912ad79875f4373070b59392b1756c8f',
            },
            'pETH-pTUSD': {
                'tokenBuy': 'ffd8d42dc40a8d166ea4848baf8b5f6e912ad79875f4373070b59392b1756c8f',
                'tokenSell': '8c3a61e77061265aaefa1e7160abfe343c2189278dd224bb7da6e7edc6a1d4db',
            },
            'PRV-pBUSD': {
                'tokenBuy': '0000000000000000000000000000000000000000000000000000000000000004',
                'tokenSell': '9e1142557e63fd20dee7f3c9524ffe0aa41198c494aa8d36447d12e85f0ddce7',
            },
            'pDAI-pTUSD': {
                'tokenBuy': 'd240c61c6066fed0535df9302f1be9f5c9728ef6d01ce88d525c4f6ff9d65a56',
                'tokenSell': '8c3a61e77061265aaefa1e7160abfe343c2189278dd224bb7da6e7edc6a1d4db',
            },
            'PRV-pUSDT': {
                'tokenBuy': '0000000000000000000000000000000000000000000000000000000000000004',
                'tokenSell': '716fd1009e2a1669caacc36891e707bfdf02590f96ebd897548e8963c95ebac0',
            },
            'PRV-pUSDC': {
                'tokenBuy': '0000000000000000000000000000000000000000000000000000000000000004',
                'tokenSell': '1ff2da446abfebea3ba30385e2ca99b0f0bbeda5c6371f4c23c939672b429a42',
            },
            'PRV-pDAI': {
                'tokenBuy': '0000000000000000000000000000000000000000000000000000000000000004',
                'tokenSell': '8c3a61e77061265aaefa1e7160abfe343c2189278dd224bb7da6e7edc6a1d4db',
            },
            'pDAI-pUSDC': {
                'tokenBuy': '8c3a61e77061265aaefa1e7160abfe343c2189278dd224bb7da6e7edc6a1d4db',
                'tokenSell': '1ff2da446abfebea3ba30385e2ca99b0f0bbeda5c6371f4c23c939672b429a42',
            },
        }
        service = PdexService()
        hours = 24
        direction = True
        result = {}
        for pairKey in commonPairs.keys():
            tokenBuy = commonPairs[pairKey].get('tokenBuy')
            tokenSell = commonPairs[pairKey].get('tokenSell')

            result[pairKey] = {}
            tokenSellData = tradeTokens.get(tokenSell)
            exchangerateSellToken = tokenSellData.get('exchange_rate')
            tokenBuyData = tradeTokens.get(tokenBuy)
            exchangerateBuyToken = tokenBuyData.get('exchange_rate')

            # get volume of last 24 hours
            result[pairKey]['volume24h'] = 0
            pair = self.lastHoursVolumeFunc(tokenBuy, tokenSell, hours, direction)
            for k in pair.keys():
                if pair[k].get('tokenId') == tokenSell:
                    result[pairKey]['volume24h'] = pair[k].get('sell') / float(exchangerateSellToken)

            # get price of last trade
            result[pairKey]['last_trade_volume'] = 0
            lastTrade = self.getLastTradingTxFunc(tokenSell=tokenSell, tokenBuy=tokenBuy)
            if lastTrade is not None:
                metadata = lastTrade.get('metadata', {})
                result[pairKey]['last_trade_volume'] = metadata.get('SellAmount', 0.0) / float(exchangerateSellToken)

            # get last trade price
            result[pairKey]['price_of_last_trade'] = 0
            txId = lastTrade.get('tx_id')
            if txId is not None and txId != '':
                trade = service.getTradingTxByRequestTxId(txId=txId)
                if trade is not None:
                    buy = (trade.get('receive_amount') / float(exchangerateBuyToken))
                    sell = (metadata.get('SellAmount', 1.0) / float(exchangerateSellToken))
                    result[pairKey]['price_of_last_trade'] = sell / buy

        return result

    def lastHoursVolume(self):
        token1 = self.params.get('token1', '')
        token2 = self.params.get('token2', '')
        # default 24 hours
        hours = self.params.get('hours', 24)
        direction = self.params.get('direction', 'false')
        direction = direction.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
        result = self.lastHoursVolumeFunc(token1, token2, hours, direction)

        for k in result.keys():
            result[k].pop('tokenId', None)
        return result

    def lastHoursVolumeFunc(self, token1, token2, hours, direction):
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
            if not direction:
                for tx in data:
                    metadata = tx['metadata']
                    if metadata[
                        'TokenIDToSellStr'] == '0000000000000000000000000000000000000000000000000000000000000004':
                        sellToken = 'PRV'
                        sellTokenId = '0000000000000000000000000000000000000000000000000000000000000004'
                    else:
                        sellToken = tokens[metadata['TokenIDToSellStr']]['name']
                        sellTokenId = metadata['TokenIDToSellStr']
                    if metadata[
                        'TokenIDToBuyStr'] == '0000000000000000000000000000000000000000000000000000000000000004':
                        buyToken = 'PRV'
                        buyTokenId = '0000000000000000000000000000000000000000000000000000000000000004'
                    else:
                        buyToken = tokens[metadata['TokenIDToBuyStr']]['name']
                        buyTokenId = metadata['TokenIDToBuyStr']
                    sellAmount = metadata['SellAmount']
                    buyAmount = tx['receive_amount']

                    if sellToken not in result:
                        result[sellToken] = 0
                    result[sellToken] += sellAmount

                    if buyToken not in result:
                        result[buyToken] = 0
                    result[buyToken] += buyAmount
            else:
                for tx in data:
                    metadata = tx['metadata']
                    if metadata[
                        'TokenIDToSellStr'] == '0000000000000000000000000000000000000000000000000000000000000004':
                        sellToken = 'PRV'
                        sellTokenId = '0000000000000000000000000000000000000000000000000000000000000004'
                    else:
                        sellToken = tokens[metadata['TokenIDToSellStr']]['name']
                        sellTokenId = metadata['TokenIDToSellStr']
                    if metadata[
                        'TokenIDToBuyStr'] == '0000000000000000000000000000000000000000000000000000000000000004':
                        buyToken = 'PRV'
                        buyTokenId = '0000000000000000000000000000000000000000000000000000000000000004'
                    else:
                        buyToken = tokens[metadata['TokenIDToBuyStr']]['name']
                        buyTokenId = metadata['TokenIDToBuyStr']
                    sellAmount = metadata['SellAmount']
                    buyAmount = tx['receive_amount']

                    if sellToken not in result:
                        result[sellToken] = {'sell': 0, 'buy': 0}
                    if buyToken not in result:
                        result[buyToken] = {'sell': 0, 'buy': 0}

                    result[sellToken]['sell'] += sellAmount
                    result[buyToken]['tokenId'] = sellTokenId
                    result[buyToken]['buy'] += buyAmount
                    result[buyToken]['tokenId'] = buyTokenId

            return result

    def updateListTokens(self):
        pdexService = PdexService()
        # get missing pdex token1
        token1 = pdexService.getMissingPdexToken1()
        # get missing pdex token 2
        token2 = pdexService.getMissingPdexToken2()

        missTokens = {}
        for t in token1:
            missTokens[t] = {}
        for t in token2:
            missTokens[t] = {}

        if len(missTokens.keys()) == 0:
            return True

        pTokens = requests.get('https://api.incognito.org/ptoken/list')
        if pTokens.status_code != 200:
            return False
        pTokens = pTokens.json().get('Result')

        temps = {}
        for t in pTokens:
            temps[t['TokenID']] = {
                'address': t['Name'],
                'rate': '1e' + str(t['Decimals']),
                'id': t['TokenID'],
            }

        for t in missTokens.keys():
            if t in temps.keys():
                missTokens[t] = temps[t]
            else:
                missTokens.pop(t, None)
        for t in missTokens:
            a = pdexService.insertPdexToken(token=missTokens[t])
            if not a:
                return False
        return True

    def leaderTraderByTradeTxs(self):
        pdexService = PdexService()
        hours = self.params.get('hours', 24)

        data = pdexService.leaderTraderByTradeTxs(last_hours=int(hours))
        return data

    def leaderTraderByVolume(self):
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
                if tx.get('trader_address_str') not in result:
                    result[tx.get('trader_address_str')] = {
                        # 'txs': 0
                    }

                # result[tx.get('trader_address_str')]['txs'] += 1

                metadata = tx['metadata']
                if metadata['TokenIDToSellStr'] == '0000000000000000000000000000000000000000000000000000000000000004':
                    sellToken = 'PRV-' + metadata['TokenIDToSellStr']
                else:
                    sellToken = tokens[metadata['TokenIDToSellStr']]['name'] + '-' + metadata['TokenIDToSellStr']
                if metadata['TokenIDToBuyStr'] == '0000000000000000000000000000000000000000000000000000000000000004':
                    buyToken = 'PRV-' + metadata['TokenIDToBuyStr']
                else:
                    buyToken = tokens[metadata['TokenIDToBuyStr']]['name'] + '-' + metadata['TokenIDToBuyStr']
                sellAmount = metadata['SellAmount']
                buyAmount = tx['receive_amount']

                if sellToken not in result[tx.get('trader_address_str')]:
                    result[tx.get('trader_address_str')][sellToken] = 0
                result[tx.get('trader_address_str')][sellToken] += sellAmount

                if buyToken not in result[tx.get('trader_address_str')]:
                    result[tx.get('trader_address_str')][buyToken] = 0
                result[tx.get('trader_address_str')][buyToken] += buyAmount

            temp = []
            for k, v in result.items():
                item = v
                keys = v.keys()
                tokenVol1 = item[keys[0]]
                tokenVol2 = item[keys[1]]
                item['volume'] = tokenVol1 * tokenVol2
                item['trader'] = k
                temp.append(item)

            temp = sorted(temp, key=itemgetter('volume'), reverse=True)

            index = 1
            for r in temp:
                result[index] = r
                index += 1

            return result

    def getPoolPair(self):
        result = []

        token1 = self.params.get('token1')
        token2 = self.params.get('token2')
        page = self.params.get('page', 0)
        limit = self.params.get('limit', 50)

        service = PdexService()
        data = service.getPoolPair(token1=token1, token2=token2, page=page, limit=limit)

        tokenService = TokenService()
        tokens = tokenService.listTokens()

        pdexToken = self.getTokens()

        for i in data:
            token1Data = tokens.get(i.get('token1_id_str'))
            token2Data = tokens.get(i.get('token2_id_str'))
            item = {
                token1Data.get('name'): i.get('token1_pool_value') / float(pdexToken.get(i.get('token1_id_str')).get(
                    'exchange_rate')),
                token2Data.get('name'): i.get('token2_pool_value') / float(pdexToken.get(i.get('token2_id_str')).get(
                    'exchange_rate')),
                'time_stamp': i.get('beacon_time_stamp'),
                'beacon_heigh': i.get('beacon_height'),
            }
            result.append(item)

        return result

    def getListTradingTxs(self):
        tokenBuy = self.params.get('token_buy')
        tokenSell = self.params.get('token_sell')

        page = self.params.get('page', 0)
        limit = self.params.get('limit', 50)

        return self.getListTradingTxsFunc(tokenBuy=tokenBuy, tokenSell=tokenSell, page=page, limit=limit)

    def getListTradingTxsFunc(self, tokenBuy='', tokenSell='', page=0, limit=50):
        service = PdexService()
        data = service.getListTradingTxs(tokenBuy=tokenBuy, tokenSell=tokenSell, page=page, limit=limit)

        result = []
        tokenService = TokenService()
        tokens = tokenService.listTokens()

        pdexToken = self.getTokens()
        for i in data:
            tokenBuyData = tokens.get(i.get('token1_id_str'))
            tokenSellData = tokens.get(i.get('token2_id_str'))

            tokenBuyValue = i.get('receive_amount') / float(pdexToken.get(i.get('token1_id_str')).get(
                'exchange_rate'))

            txMetadata = i.get('tx_metadata')
            tokenSellValue = txMetadata.get('SellAmount') / float(pdexToken.get(i.get('token2_id_str')).get(
                'exchange_rate'))

            item = {
                'id': i.get('requested_tx_id'),
                'timestamp': i.get('beacon_time_stamp').strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'price': str(tokenSellValue / tokenBuyValue),
                'amount': str(tokenSellValue),
                'amount_quote': str(tokenBuyValue),
            }
            result.append(item)

        return result
