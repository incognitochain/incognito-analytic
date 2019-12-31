import requests

from service.blockservice import BlockService
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
