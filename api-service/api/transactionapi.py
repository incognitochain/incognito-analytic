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
