package models

type Token struct {
	ID         int     `db:"id"`
	TokenID    string  `db:"token_id"`
	Name       string  `db:"name"`
	Symbol     string  `db:"symbol"`
	CountTx    int     `db:"count_tx"`
	Supply     uint64  `db:"supply"`
	ListHashTx *string `db:"list_hash_tx"`
	Data       string  `db:"data"`
	Info       string  `db:info`
}
