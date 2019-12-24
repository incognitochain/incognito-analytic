from sqlalchemy import create_engine

from service import SQLALCHEMY_DATABASE_URI

db = create_engine(SQLALCHEMY_DATABASE_URI)


class TokenService:
    def listTokens(self):
        sql = """
            SELECT token_id, name, symbol, count_tx, supply FROM tokens
        """
        resultSet = db.execute(sql)
        result = {}
        for r in resultSet:
            result[r[0]] = {
                "name": r[1],
                "symbol": r[2],
                "count_tx": r[3],
                "supply": r[4]
            }
        return result
