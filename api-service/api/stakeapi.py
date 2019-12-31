from service.blockservice import BlockService


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
