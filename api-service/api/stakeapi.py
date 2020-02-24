import requests

from service.blockservice import BlockService
from service.pdexservice import PdexService
from service.token import TokenService
from service.transactionservice import TransactionService


class StakeAPI():
    def __init__(self, requestParams):
        self.params = requestParams

    def get(self):
        return "Token API"

    def getMinedPRVToken(self):
        blockService = BlockService()
        data = blockService.countShardBlock(shard_id=-1)
        minedPRVToken = 0
        for k in data:
            minedPRVToken += (data[k] - 1) * 1386666000
        return minedPRVToken

    def getTotalStakedTokens(self):
        txService = TransactionService()

        stakingTxs = txService.listStakingTxs()
        total = 0
        for v in stakingTxs:
            total += v.get('metadata').get('StakingAmountShard')
        return total

    def prvFee(self):
        txService = TransactionService()
        return txService.sumPRVFee()

    def dailyPrvFee(self):
        txService = TransactionService()
        fromDate = self.params.get('from_date', '')
        toDate = self.params.get('to_date', '')
        limit = self.params.get('limit', 0)
        page = self.params.get('page', 0)
        data = txService.dailyPRVFee(fromDate=fromDate, toDate=toDate, page=int(page), limit=int(limit))
        return data

    def tokenFee(self):
        txService = TransactionService()

        tokenID = self.params.get('token_id', '')

        tokenServie = TokenService()
        tokens = tokenServie.listTokens()

        tokenName = tokens.get(tokenID).get('name')

        pdexService = PdexService()
        pdexTokens = pdexService.getTokens()

        data = txService.sumTokenFee(tokenID=tokenID)
        result = {
            'name': tokenName,
            'fee': data[tokenID] / float(pdexTokens.get(tokenID).get('exchange_rate')),
            'id': tokenID,
            'rate': pdexTokens.get(tokenID).get('exchange_rate'),
        }
        return result
