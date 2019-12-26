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
