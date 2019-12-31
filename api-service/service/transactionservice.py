from sqlalchemy import create_engine

from service import SQLALCHEMY_DATABASE_URI

db = create_engine(SQLALCHEMY_DATABASE_URI)


class TransactionService:
    def getAvgPRVFee(self):
        result_set = db.execute("""
                    SELECT avg(transactions.prv_fee) FROM transactions WHERE transactions.prv_fee > 0
                """)
        for r in result_set:
            return float(r[0])
        return 0

    def getAvgFeeToken(self, tokenID):
        result_set = db.execute("""
        SELECT transactions.transacted_privacy_coin ->> 'PropertyID' AS property_id, AVG(transactions.transacted_privacy_coin_fee) FROM transactions 
        WHERE 
            transactions.transacted_privacy_coin_fee > 0 OR 1 = 1
        AND 
            CAST(transactions.transacted_privacy_coin ->> 'PropertyID' as TEXT) = '""" + tokenID + """'
        GROUP BY transactions.transacted_privacy_coin ->> 'PropertyID'
        """)

        for r in result_set:
            return float(r[1])
        return 0

    def listTxByMetadataType(self, metadataType, page=0, limit=10, order_trend='ASC', bridgeTokenID='',
                             deBridgeTokenID=''):
        pagenator = """"""
        if limit > 0:
            pagenator = """
                OFFSET """ + str(page * limit) + """
                LIMIT """ + str(limit)
        byBridgeTokenID = """"""
        if bridgeTokenID != '':
            byBridgeTokenID = """ AND CAST(t.metadata ->> 'TokenID' as TEXT) = '""" + bridgeTokenID + """'"""

        byDeBridgeTokenID = """"""
        if deBridgeTokenID != '':
            if metadataType == 80:
                byDeBridgeTokenID = """ AND CAST(t.metadata ->> 'IncTokenID' as TEXT) = '""" + deBridgeTokenID + """'"""
            else:
                byDeBridgeTokenID = """ AND CAST(t.metadata ->> 'TokenID' as TEXT) = '""" + deBridgeTokenID + """'"""

        sql = """
                SELECT t.tx_id, t.metadata FROM transactions as t
                WHERE CAST(t.metadata ->> 'Type' as INT) = """ + str(metadataType) + byBridgeTokenID + byDeBridgeTokenID \
              + pagenator + """
                ORDER BY t.created_time """ + order_trend + """
        """
        result_set = db.execute(sql)
        txs = []
        for r in result_set:
            tx = {
                'tx_id': r[0],
                'metadata': r[1],
            }
            txs.append(tx)
        return txs

    def getTxByHash(self, hash=''):
        if hash == '':
            return {}

        sql = """SELECT data from transactions WHERE tx_id='""" + hash + """' """
        data = db.execute(sql)
        for r in data:
            return r[0]

    def countTx(self):
        sql = """SELECT shard_id, max(block_height), count(tx_id), max(created_time) from transactions group by shard_id order by shard_id"""
        data = db.execute(sql)
        result = {}
        for r in data:
            result[r[0]] = {
                'last_block_height': r[1],
                'count': r[2],
                'last_created_time': r[3]
            }
        return result

    def listStakingTxs(self):
        sql = """
            SELECT tx_id, tx_version, shard_id, tx_type, prv_fee, proof_detail, metadata, created_time FROM transactions WHERE CAST(metadata->>'Type' as INT) = 63
        """
        data = db.execute(sql)
        result = []
        for r in data:
            result.append({
                'tx_id': r[0],
                'metadata': r[6],
                'created_time': r[7],
            })
        return result

    def sumPRVFee(self):
        sql = """
            select sum(prv_fee) from transactions where prv_fee > 0 and prv_fee is not null
        """
        data = db.execute(sql)
        for r in data:
            return r[0]

    def sumTokenFee(self, tokenID=''):
        if tokenID == '':
            return {}
        sql = """
            select cast(transacted_privacy_coin->>'PropertyID' as text) as token_id, transacted_privacy_coin, transacted_privacy_coin_fee  from transactions where transacted_privacy_coin_fee > 0 and transacted_privacy_coin_fee is not null and cast(transacted_privacy_coin->>'PropertyID' as text) = '""" + tokenID + """'
        """

        data = db.execute(sql)
        result = {}
        for r in data:
            if r[0] not in result.keys():
                result[r[0]] = 0
            result[r[0]] += r[2]
        return result
