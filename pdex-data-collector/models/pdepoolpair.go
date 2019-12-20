package models

import "time"

type PDEPoolPair struct {
	ID                  string    `db:"id"`
	Token1IDStr         string    `db:"token1_id_str"`
	Token1PoolValue     uint64    `db:"token1_pool_value"`
	Token2IDStr         string    `db:"token2_id_str"`
	Token2PoolValue     uint64    `db:"token2_pool_value"`
	Token1ToToken2Price uint64    `db:"token1_to_token2_price"`
	Token2ToToken1Price uint64    `db:"token2_to_token1_price"`
	BeaconHeight        uint64    `db:"beacon_height"`
	BeaconTimeStamp     time.Time `db:"beacon_time_stamp"`
}
