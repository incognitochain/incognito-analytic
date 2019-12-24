from service.token import TokenService


class TokenAPI():

    def __init__(self, requestParams):
        self.params = requestParams

    def get(self):
        return "Token API"

    def listTokens(self):
        service = TokenService()
        return service.listTokens()