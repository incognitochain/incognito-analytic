from service.blockservice import BlockService


class BlockAPI():
    def __init__(self, requestParams):
        self.params = requestParams

    def get(self):
        return "Block API"

    def countBeaconBlock(self):
        blockService = BlockService()
        return blockService.countBeaconBlock()

    def lastBeaconBlock(self):
        blockService = BlockService()
        return blockService.lastBeaconBlock()

    def listBeaconBlock(self):
        blockService = BlockService()
        page = self.params.get('page', 0)
        limit = self.params.get('limit', 0)
        return blockService.listBeaconBlock(page=int(page), limit=int(limit))

    def getBeaconBlock(self):
        blockService = BlockService()
        blockHeight = self.params.get('block_height', 0)
        blockHash = self.params.get('block_hash', '')
        return blockService.getBeaconBlock(block_height=int(blockHeight), block_hash=blockHash)
