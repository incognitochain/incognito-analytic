package entities

type TransactionDetail struct {
	BlockHash   string `json:"BlockHash"`
	BlockHeight uint64 `json:"BlockHeight"`
	Index       uint64 `json:"Index"`
	ShardID     byte   `json:"ShardID"`
	Hash        string `json:"Hash"`
	Version     int8   `json:"Version"`
	Type        string `json:"Type"` // Transaction type
	LockTime    string `json:"LockTime"`
	Fee         uint64 `json:"Fee"` // Fee applies: always consant
	Image       string `json:"Image"`

	IsPrivacy       bool        `json:"IsPrivacy"`
	Proof           string      `json:"Proof"`
	ProofDetail     ProofDetail `json:"ProofDetail"`
	InputCoinPubKey string      `json:"InputCoinPubKey"`
	SigPubKey       string      `json:"SigPubKey,omitempty"` // 64 bytes
	Sig             string      `json:"Sig,omitempty"`       // 64 bytes

	Metadata                      string      `json:"Metadata"`
	CustomTokenData               string      `json:"CustomTokenData"`
	PrivacyCustomTokenID          string      `json:"PrivacyCustomTokenID"`
	PrivacyCustomTokenName        string      `json:"PrivacyCustomTokenName"`
	PrivacyCustomTokenSymbol      string      `json:"PrivacyCustomTokenSymbol"`
	PrivacyCustomTokenData        string      `json:"PrivacyCustomTokenData"`
	PrivacyCustomTokenProofDetail ProofDetail `json:"PrivacyCustomTokenProofDetail"`
	PrivacyCustomTokenIsPrivacy   bool        `json:"PrivacyCustomTokenIsPrivacy"`
	PrivacyCustomTokenFee         uint64      `json:"PrivacyCustomTokenFee"`

	IsInMempool bool `json:"IsInMempool"`
	IsInBlock   bool `json:"IsInBlock"`

	Info string `json:"Info"`
}

type ProofDetail struct {
	InputCoins  []*CoinDetail
	OutputCoins []*CoinDetail
}

type CoinDetail struct {
	CoinDetails          Coin
	CoinDetailsEncrypted string
}

type Coin struct {
	PublicKey      string
	CoinCommitment string
	SerialNumber   string
	Value          uint64
	Info           string
}

type TransactionDetailRes struct {
	RPCBaseRes
	Result *TransactionDetail
}
