package postgresql

import (
	"github.com/incognitochain/incognito-analytic/pdex-data-collector/models"

	_ "github.com/lib/pq"
)

// BeaconBlockStore is Beacon Block postgresql store
type BeaconBlockStore struct {
	PGStoreAbs
}

// NewBeaconBlockStore initialises BeaconBlockStore with pg connection
func NewBeaconBlockStore() (*BeaconBlockStore, error) {
	pgConn, err := getPGConnection()
	if err != nil {
		return nil, err
	}
	store := &BeaconBlockStore{}
	store.DB = pgConn
	return store, nil
}

func (st *BeaconBlockStore) GetLatestProcessedBCHeight() (uint64, error) {
	sqlStr := `
		SELECT block_height FROM beacon_blocks
		ORDER BY beacon_height DESC
		LIMIT 1
	`
	bcHeights := []uint64{}
	err := st.DB.Select(&bcHeights, sqlStr)
	if err != nil {
		return 0, err
	}
	if len(bcHeights) == 0 {
		return 0, nil
	}
	return bcHeights[0], nil
}

func (st *BeaconBlockStore) StoreBeaconBlock(beaconBlockModel *models.BeaconBlock) error {
	sqlStr := `
		INSERT INTO beacon_blocks (block_hash, block_heigh, data, instructions, pre_block, next_block, created_time, block_version, epoch, round)
		VALUES (:block_hash, :block_heigh, :data, :instructions, :pre_block, :next_block, :created_time, :block_version, :epoch, :round)
		RETURNING id
	`
	tx := st.DB.MustBegin()
	defer tx.Commit()
	_, err := tx.NamedQuery(sqlStr, beaconBlockModel)
	return err
}
