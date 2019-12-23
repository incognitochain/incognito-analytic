package models

import "time"

type BeaconBlock struct {
	ID           string `data:"id"`
	BlockHash    string `data:"block_hash"`
	BlockHeight  uint64 `data:"block_height"`
	BlockVersion int    `data:"block_version"`
	Epoch        uint64 `data:"epoch"`
	Round        int    `data:"round"`

	Data         string    `data:"data"`
	Instructions string    `data:"instructions"`
	PreBlock     string    `data:"pre_block"`
	NextBlock    string    `data:"next_block"`
	CreatedTime  time.Time `data:"created_time"`
}
