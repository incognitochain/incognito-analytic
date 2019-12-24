package entities

type CustomToken struct {
	ID                 string   `json:"ID"`
	Name               string   `json:"Name"`
	Symbol             string   `json:"Symbol"`
	Image              string   `json:"Image"`
	Amount             uint64   `json:"Amount"`
	IsPrivacy          bool     `json:"IsPrivacy"`
	ListTxs            []string `json:"ListTxs"`
	CountTxs           int      `json:"CountTxs"`
	InitiatorPublicKey string   `json:"InitiatorPublicKey"`
	TxInfo             string   `json:"TxInfo"`
}

type ListCustomToken struct {
	ListCustomToken []CustomToken `json:"ListCustomToken"`
}

type ListCustomTokenRes struct {
	RPCBaseRes
	Result *ListCustomToken
}

type CustomTokenRes struct {
	RPCBaseRes
	Result *CustomToken
}
