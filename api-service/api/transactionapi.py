import json
from flask_restful import Resource

from service.transaction import TransactionService


class TransactionAPI():

    def __init__(self, requestParams):
        self.params = requestParams

    def get(self):
        return "Transaction API"

    def getAvgFee(self):
        service = TransactionService()
        tokenID = ''
        if hasattr(self, 'params') and 'token_id' in self.params:
            tokenID = self.params['token_id']
        if tokenID == '':
            return {"PRV": service.getAvgPRVFee()}
        else:
            return {tokenID: service.getAvgFeeToken(tokenID)}

    def listWithdrawLiquidityTx(self):

        page = self.params.get('page', 0)
        limit = self.params.get('limit', 0)
        group = self.params.get('group', 0)
        order_trend = self.params.get('order_trend', 'ASC')

        service = TransactionService()
        txs = service.listTxByMetadataType(metadataType=93, page=int(page), limit=int(limit), order_trend=order_trend)
        if int(group) == 1:
            result = {}
            for tx in txs:
                PDEContributionPairID = tx['metadata']['PDEContributionPairID']
                if PDEContributionPairID not in result:
                    result[PDEContributionPairID] = []
                result[PDEContributionPairID].append(tx)
            return result
        else:
            result = []
            for tx in txs:
                result.append(tx)
            return json.dumps(result)
