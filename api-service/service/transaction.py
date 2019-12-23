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
