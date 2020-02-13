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
        result['0000000000000000000000000000000000000000000000000000000000000004'] = {'symbol': 'PRV',
                                                                                      'name': 'Privacy'}
        return result

    def listTokenTxs(self, tokenId):
        sql = """
                    SELECT list_hash_tx FROM tokens WHERE token_id='""" + tokenId + """'
                """
        resultSet = db.execute(sql)
        result = []
        for r in resultSet:
            result = r[0]
        return result

    def tokenInitTx(self, tokenId):
        sql = """
        select transactions.data from transactions
        where transactions.tx_id in (
            select json_array_elements_text(tokens.list_hash_tx) from tokens where tokens.token_id = '""" + tokenId + """'
        )
        order by created_time asc
        limit 1
        """

        resultSet = db.execute(sql)
        for r in resultSet:
            return r[0]
