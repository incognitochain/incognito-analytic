package postgresql

import (
	"github.com/incognitochain/incognito-analytic/pdex-data-collector/models"
	_ "github.com/lib/pq"
)

// BeaconBlockStore is Beacon Block postgresql store
type ShardBlockStore struct {
	PGStoreAbs
}

// NewBeaconBlockStore initialises BeaconBlockStore with pg connection
func NewShardBlockStore() (*ShardBlockStore, error) {
	pgConn, err := getPGConnection()
	if err != nil {
		return nil, err
	}
	store := &ShardBlockStore{}
	store.DB = pgConn
	return store, nil
}

func (st *ShardBlockStore) GetLatestProcessedBCHeight(shardID int) (uint64, error) {
	sqlStr := `
		SELECT block_height FROM shard_blocks
		WHERE shard_id=:shar_id
		ORDER BY beacon_height DESC
		LIMIT 1
	`
	bcHeights := []uint64{}
	err := st.DB.Select(&bcHeights, sqlStr, shardID)
	if err != nil {
		return 0, err
	}
	if len(bcHeights) == 0 {
		return 0, nil
	}
	return bcHeights[0], nil
}

func (st *ShardBlockStore) StoreShardBloc(beaconBlockModel *models.ShardBlock) error {
	sqlStr := `
		INSERT INTO shard_blocks (block_hash, created_time, data, count_tx, shard_id, block_height, block_producer, pre_block, next_block, list_hash_tx, beacon_block_height, block_version, epoch, round)
		VALUES (:block_hash, :created_time, :data, :count_tx, :shard_id, :block_height, :block_producer, :pre_block, :next_block, :list_hash_tx, :beacon_block_height, :block_version, :epoch, :round)
		RETURNING id
	`
	tx := st.DB.MustBegin()
	defer tx.Commit()
	_, err := tx.NamedQuery(sqlStr, beaconBlockModel)
	return err
}
