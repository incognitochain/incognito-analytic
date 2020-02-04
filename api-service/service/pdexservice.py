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

    def countTradingTxs(self):
        sql = """
            SELECT count(requested_tx_id) FROM pde_trades
        """

        result_set = db.execute(sql)
        for r in result_set:
            return r[0]

    def lastTradingTx(self, tokenSell="", tokenBuy=""):
        sql = """
            SELECT tx_id, shard_id, prv_fee, info, block_height, block_hash, metadata, transacted_privacy_coin_fee, created_time FROM transactions WHERE tx_id in (
                SELECT requested_tx_id FROM pde_trades order by beacon_height desc limit 1
            )
        """

        if tokenSell != "" and tokenBuy != "":
            sql = """
                        SELECT tx_id, shard_id, prv_fee, info, block_height, block_hash, metadata, transacted_privacy_coin_fee, created_time FROM transactions WHERE tx_id in (
                            SELECT requested_tx_id FROM pde_trades WHERE receiving_tokenid_str='""" + tokenBuy + """' 
                            AND (token2_id_str='""" + tokenSell + """' OR token1_id_str='""" + tokenSell + """') ORDER BY beacon_height desc limit 1
                        )
                    """

        result_set = db.execute(sql)
        for r in result_set:
            return {
                "tx_id": r[0],
                "shard_id": r[1],
                "prv_fee": r[2],
                "info": r[3],
                "block_height": r[4],
                "block_hash": r[5],
                "metadata": r[6],
                "transacted_privacy_coin_fee": r[7],
                "created_time": r[8],
            }
        return {}

    def lastTradingTxInHours(self, token1, token2, hours=24):
        sql = """
                SELECT t.tx_id, t.metadata,  p.receive_amount, p.trader_address_str
                FROM pde_trades p
                JOIN transactions t ON t.created_time >= NOW() - INTERVAL '""" + str(hours) + """ HOURS' and t.tx_id = p.requested_tx_id
                WHERE (p.token1_id_str = '""" + token2 + """' AND p.token2_id_str = '""" + token1 + """')
                OR (p.token1_id_str = '""" + token1 + """' AND p.token2_id_str = '""" + token2 + """')
                AND p.status = 'accepted'
                ORDER BY t.created_time DESC
        """

        result_set = db.execute(sql)
        result = []
        for r in result_set:
            item = {
                'tx_id': r[0],
                'metadata': r[1],
                'receive_amount': r[2],
                'trader_address_str': r[3],
            }
            result.append(item)
        return result

    def getMissingPdexToken1(self):
        sql = """
            SELECT DISTINCT(token1_id_str) FROM pde_pool_pairs pp 
            WHERE 
            token1_id_str NOT IN (
                SELECT address FROM pde_token_name
            )
        """

        data = db.execute(sql)
        result = []
        for r in data:
            result.append(r[0])
        return result

    def getMissingPdexToken2(self):
        sql = """
            SELECT DISTINCT(token2_id_str) FROM pde_pool_pairs pp 
            WHERE 
            token2_id_str NOT IN (
                SELECT address FROM pde_token_name
            )
        """

        data = db.execute(sql)
        result = []
        for r in data:
            result.append(r[0])
        return result

    def insertPdexToken(self, token=None):
        if token == None:
            return False

        sql = """INSERT INTO pde_token_name (address, name, exchange_rate) VALUES(%s, %s, %s)"""
        db.execute(sql, (token['id'], token['address'], token['rate']))
        return True

    def leaderTraderByTradeTxs(self, last_hours=24):
        sql = """
        select pt.trader_address_str, count(*) from pde_trades pt
        join transactions t on t.tx_id = pt.requested_tx_id and t.created_time >= NOW() - INTERVAL '""" \
              + str(last_hours) + """ HOURS'
        group by pt.trader_address_str
        order by count(*) desc
        """

        data = db.execute(sql)
        result = {}
        index = 1
        for r in data:
            item = {
                'trader': r[0],
                'txs': r[1],
            }
            result[index] = item
            index += 1

        return result
