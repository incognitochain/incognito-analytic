package models

type PDETrade struct {
	TraderAddressStr    string `db:"trader_address_str"`
	ReceivingTokenIDStr string `db:"receiving_tokenid_str"`
	ReceiveAmount       uint64 `db:"receive_amount"`
	Token1IDStr         string `db:"token1_id_str"`
	Token2IDStr         string `db:"token2_id_str"`
	ShardID             byte   `db:"shard_id"`
	RequestedTxID       string `db:"requested_tx_id"`
	Status              string `db:"status"`
	BeaconHeight        uint64 `db:"beacon_height"`
}
