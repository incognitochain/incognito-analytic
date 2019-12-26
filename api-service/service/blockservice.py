from sqlalchemy import create_engine

from service import SQLALCHEMY_DATABASE_URI

db = create_engine(SQLALCHEMY_DATABASE_URI)


class BlockService:
    def countBeaconBlock(self):
        sql = """
            SELECT COUNT(block_height) FROM beacon_blocks
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
