from service.token import TokenService
import json


class TokenAPI():

    def __init__(self, requestParams):
        self.params = requestParams

    def get(self):
        return "Token API"

    def listTokens(self):
        service = TokenService()
        return service.listTokens()

    def listTokenTxs(self):
        service = TokenService()
        tokenId = self.params['token_id']
        data = service.listTokenTxs(tokenId)
        return data

    def tokenInitTx(self):
        service = TokenService()
        tokenId = self.params['token_id']
        data = service.tokenInitTx(tokenId=tokenId)
        return data
