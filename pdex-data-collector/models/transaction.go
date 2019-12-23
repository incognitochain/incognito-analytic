package models

import "time"

type Transaction struct {
	ID        string `json:"id"`
	TxID      string `json:"tx_id"`
	TxVersion int    `json:"tx_version"`
	TxType    string `json:"tx_type"`

	Data                             string    `json:"data"`
	ShardID                          int       `json:"shard_id"`
	PRVFee                           float64   `json:"prv_fee"`
	Info                             string    `json:"info"`
	Proof                            string    `json:"proof"`
	ProofDetail                      string    `json:"proof_detail"`
	Metadata                         string    `json:"metadata"`
	TransactedPrivacyCoin            string    `json:"transacted_privacy_coin"`
	TransactedPrivacyCoinProofDetail string    `json:"transacted_privacy_coin_proof_detail"`
	TransactedPrivacyCoinFee         float64   `json:"transacted_privacy_coin_fee"`
	CreatedTime                      time.Time `json:"created_time"`
	BlockHeight                      uint64    `json:"block_height"`
	BlockHash                        string    `json:"block_hash"`
}
