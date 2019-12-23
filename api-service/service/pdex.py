from flask import jsonify
from sqlalchemy import create_engine

from service import SQLALCHEMY_DATABASE_URI

db = create_engine(SQLALCHEMY_DATABASE_URI)


class PdexService:
    def getTradingPairs(self):
        result_set = db.execute("""
            SELECT distinct token1_id_str, token2_id_str FROM pde_pool_pairs
        """)

        pairs = []
        tokens = self.getTokens()
        for r in result_set:
            token1 = r[0]
            token2 = r[1]
            if token2 in tokens and token1 in tokens:
                pair = {
                    token1: tokens[token1],
                    token2: tokens[token2],
                }
                pairs.append(pair)
        return pairs

    def getTokens(self):
        sql = """
            SELECT address, name, exchange_rate FROM pde_token_name
        """
        result_set = db.execute(sql)
        tokens = {}
        for r in result_set:
            tokens[r[0]] = {"name": r[1], "exchange_rate": r[2]}
        return tokens
