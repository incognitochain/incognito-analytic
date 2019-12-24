package models

type Token struct {
	ID         int    `json:"id"`
	TokenID    string `json:"token_id"`
	Name       string `json:"name"`
	Symbol     string `json:"symbol"`
	CountTx    int    `json:"count_tx"`
	Supply     int    `json:"supply"`
	ListHashTx string `json:"list_hash_tx"`
}
