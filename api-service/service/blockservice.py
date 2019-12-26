from sqlalchemy import create_engine

from service import SQLALCHEMY_DATABASE_URI

db = create_engine(SQLALCHEMY_DATABASE_URI)


class BlockService:
    def countBeaconBlock(self):
        sql = """
            SELECT COUNT(distinct(block_height)) FROM beacon_blocks
        """
        resultSet = db.execute(sql)
        for r in resultSet:
            return r[0]

    def lastBeaconBlock(self):
        sql = """
            SELECT data FROM beacon_blocks ORDER BY block_height DESC LIMIT 1
        """
        resultSet = db.execute(sql)
        for r in resultSet:
            return r[0]

    def listBeaconBlock(self, page=0, limit=0):
        pagenator = """"""
        if limit > 0:
            pagenator = """
                        OFFSET """ + str(page * limit) + """
                        LIMIT """ + str(limit)

        sql = """SELECT block_height, block_hash, created_time, CAST(data ->> 'BlockProducer' as TEXT) as block_producer, data FROM beacon_blocks as b ORDER BY b.block_height desc """ \
              + pagenator

        dataSet = db.execute(sql)
        result = []
        for r in dataSet:
            item = {
                'block_height': r[0],
                'block_hash': r[1],
                'created_time': r[2],
                'block_producer': r[3],
                'data': r[4]
            }
            result.append(item)
        return result

    def getBeaconBlock(self, block_height=0, block_hash=""):
        if block_height == 0 and block_hash == "":
            return {}

        sql = """SELECT data FROM beacon_blocks WHERE block_height=""" + str(
            block_height) + """ OR block_hash='""" + block_hash + """'"""
        dataSet = db.execute(sql)
        for r in dataSet:
            return r[0]
