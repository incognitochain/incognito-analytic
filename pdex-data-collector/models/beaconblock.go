package models

import "time"

type BeaconBlock struct {
	ID           string `db:"id"`
	BlockHash    string `db:"block_hash"`
	BlockHeight  uint64 `db:"block_height"`
	BlockVersion int    `db:"block_version"`
	Epoch        uint64 `db:"epoch"`
	Round        int    `db:"round"`

	Data         string    `db:"data"`
	Instructions string    `db:"instructions"`
	PreBlock     string    `db:"pre_block"`
	NextBlock    string    `db:"next_block"`
	CreatedTime  time.Time `db:"created_time"`
}
