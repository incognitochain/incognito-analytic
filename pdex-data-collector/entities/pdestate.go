package entities

type PDEContribution struct {
	ContributorAddressStr string
	TokenIDStr            string
	Amount                uint64
	TxReqID               string
}

type PDEPoolForPair struct {
	Token1IDStr     string
	Token1PoolValue uint64
	Token2IDStr     string
	Token2PoolValue uint64
}

type PDEState struct {
	WaitingPDEContributions map[string]*PDEContribution
	PDEPoolPairs            map[string]*PDEPoolForPair
	PDEShares               map[string]uint64
}

type PDEStateRes struct {
	RPCBaseRes
	Result *PDEState
}
