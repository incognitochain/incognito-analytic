package postgresql

import (
	"github.com/incognitochain/incognito-analytic/incognito-data-collector/models"

	_ "github.com/lib/pq"
)

// PDEInstructionsPGStore is PDE instructions postgresql store
type PDEInstructionsPGStore struct {
	PGStoreAbs
}

// NewPDEInstructionsPGStore initialises PDEStatePGStore with pg connection
func NewPDEInstructionsPGStore() (*PDEInstructionsPGStore, error) {
	pgConn, err := getPGConnection()
	if err != nil {
		return nil, err
	}
	store := &PDEInstructionsPGStore{}
	store.DB = pgConn
	return store, nil
}

func (is *PDEInstructionsPGStore) EnsurePDEInstructionsPGStore() {
	// TODO: implement it
}

func (is *PDEInstructionsPGStore) GetLatestProcessedBCHeight() (uint64, error) {
	sqlStr := `
		SELECT beacon_height FROM pde_trades
		ORDER BY beacon_height DESC
		LIMIT 1
	`
	bcHeights := []uint64{}
	err := is.DB.Select(&bcHeights, sqlStr)
	if err != nil {
		return 0, err
	}
	if len(bcHeights) == 0 {
		return 0, nil
	}
	return bcHeights[0], nil
}

func (is *PDEInstructionsPGStore) StorePDETrade(tradeModel *models.PDETrade) error {
	sqlStr := `
		INSERT INTO pde_trades (
			trader_address_str,
			receiving_tokenid_str,
			receive_amount,
			token1_id_str,
			token2_id_str,
			shard_id,
			requested_tx_id,
			status,
			beacon_height,
			beacon_time_stamp
		)
		VALUES (
			:trader_address_str,
			:receiving_tokenid_str,
			:receive_amount,
			:token1_id_str,
			:token2_id_str,
			:shard_id,
			:requested_tx_id,
			:status,
			:beacon_height,
			:beacon_time_stamp
		)
		RETURNING id
	`
	tx := is.DB.MustBegin()
	defer tx.Commit()
	_, err := tx.NamedQuery(sqlStr, tradeModel)
	return err
}
