package postgresql

import "github.com/incognitochain/incognito-analytic/pdex-data-collector/models"

// BeaconBlockStore is Beacon Block postgresql store
type TransactionsStore struct {
	PGStoreAbs
}

// NewBeaconBlockStore initialises BeaconBlockStore with pg connection
func NewTransactionsStore() (*TransactionsStore, error) {
	pgConn, err := getPGConnection()
	if err != nil {
		return nil, err
	}
	store := &TransactionsStore{}
	store.DB = pgConn
	return store, nil
}

func (st *TransactionsStore) GetLatestProcessedShardHeight(shardID int) (uint64, error) {
	sqlStr := `
		SELECT block_height FROM transactions
		WHERE shard_id=$1
		ORDER BY block_height DESC
		LIMIT 1
	`
	blockHeights := []uint64{}
	err := st.DB.Select(&blockHeights, sqlStr, shardID)
	if err != nil {
		return 0, err
	}
	if len(blockHeights) == 0 {
		return 0, nil
	}
	return blockHeights[0], nil
}

func (st *TransactionsStore) LatestProcessedTxByHeight(shardID int, blockHeight uint64) ([]string, error) {
	sql := `
		SELECT tx_id FROM transactions WHERE shard_id = $1 AND block_height = $2
	`
	result := []string{}
	err := st.DB.Select(&result, sql, shardID, blockHeight)
	if err != nil {
		return result, err
	}
	return result, err
}

type ListProcessingTx struct {
	BlockHeight uint64
	BlockHash   string
	ShardID     int
	TxsHash     []string
}

func (st *TransactionsStore) ListProcessingTxByHeight(shardID int, blockHeight uint64) (*ListProcessingTx, error) {
	sqlStr := `
		SELECT shardblock.block_height as BlockHeight, 
		shardblock.shard_id as ShardID, 
		shardblock.block_hash as BlockHash,  
		shardblock.list_hash_tx as TxsHash 
		
		FROM shard_blocks shardblock
		
		WHERE shard_id = $1 AND json_array_length(shardblock.list_hash_tx) > 0 AND block_height = $2
		
		ORDER BY block_height DESC
	`
	result := []*ListProcessingTx{}
	err := st.DB.Select(&result, sqlStr, shardID, blockHeight)
	if err != nil {
		return nil, err
	}
	if len(result) > 0 {
		return result[0], err
	} else {
		return nil, nil
	}
}

func (st *TransactionsStore) ListNeedProcessingTxByHeight(shardID int, blockHeight uint64) ([]*ListProcessingTx, error) {
	sqlStr := `
		SELECT shardblock.block_height as BlockHeight, 
		shardblock.shard_id as ShardID, 
		shardblock.block_hash as BlockHash,  
		shardblock.list_hash_tx as TxsHash 
		
		FROM shard_blocks shardblock
		
		WHERE shard_id = $1 AND json_array_length(shardblock.list_hash_tx) > 0 AND block_height >= $2
		
		ORDER BY block_height DESC
	`
	result := []*ListProcessingTx{}
	err := st.DB.Select(&result, sqlStr, shardID, blockHeight)
	if err != nil {
		return nil, err
	}
	if len(result) > 0 {
		return result, err
	} else {
		return nil, nil
	}
}

func (st *TransactionsStore) GetTransactionById(txID string) (*models.Transaction, error) {
	sql := `SELECT * FROM transactions WHERE tx_id=$1`
	result := []*models.Transaction{}
	err := st.DB.Select(&result, sql, txID)
	if err != nil {
		return nil, err
	} else {
		if len(result) == 0 {
			return nil, nil
		}
		return result[0], nil
	}
}

func (st *TransactionsStore) StoreTransaction(txs *models.Transaction) error {
	sqlStr := `
		INSERT INTO shard_blocks (data, tx_id, tx_version, shard_id, tx_type, prv_fee, info, proof, proof_detail, metadata, transacted_privacy_coin, transacted_privacy_coin_proof_detail, transacted_privacy_coin_fee, created_time, block_height, block_hash)
		VALUES (:data, :tx_id, :tx_version, :shard_id, :tx_type, :prv_fee, :info, :proof, :proof_detail, :metadata, :transacted_privacy_coin, :transacted_privacy_coin_proof_detail, :transacted_privacy_coin_fee, :created_time, :block_height, :block_hash)
		RETURNING id
	`
	tx := st.DB.MustBegin()
	defer tx.Commit()
	_, err := tx.NamedQuery(sqlStr, txs)
	return err
}
