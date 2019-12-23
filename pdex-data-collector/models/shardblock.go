package models

import (
	"time"
)

type ShardBlock struct {
	ID            string `json:"id"`
	BlockHash     string `json:"block_hash"`
	BlockVersion  int    `json:"block_version"`
	BlockHeight   uint64 `json:"block_height"`
	BlockProducer string `json:"block_producer"`
	Epoch         uint64 `data:"epoch"`
	Round         uint64 `data:"round"`

	CreatedTime      time.Time `json:"created_time"`
	Data             string    `json:"data"`
	CountTx          uint64    `json:"count_tx"`
	ShardID          int       `json:"shard_id"`
	PreBlock         string    `json:"pre_block"`
	NextBlock        string    `json:"next_block"`
	ListHashTx       string    `json:"list_hash_tx"`
	BeaconBlockHeigh uint64    `json:"beacon_block_heigh"`
}
