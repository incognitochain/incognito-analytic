package entities

type PDEWithdrawalInst struct {
	WithdrawalTokenIDStr string
	WithdrawerAddressStr string
	DeductingPoolValue   uint64
	DeductingShares      uint64
	PairToken1IDStr      string
	PairToken2IDStr      string
	TxReqID              string
	ShardID              byte
	Status               string
	BeaconHeight         uint64
}

type PDETradeInst struct {
	TraderAddressStr    string
	ReceivingTokenIDStr string
	ReceiveAmount       uint64
	Token1IDStr         string
	Token2IDStr         string
	ShardID             byte
	RequestedTxID       string
	Status              string
	BeaconHeight        uint64
}

type PDEContributionInst struct {
	PDEContributionPairID string
	ContributorAddressStr string
	ContributedAmount     uint64
	TokenIDStr            string
	TxReqID               string
	ShardID               byte
	Status                string
	BeaconHeight          uint64
}

type PDEInfoFromBeaconBlock struct {
	PDEContributions []*PDEContributionInst
	PDETrades        []*PDETradeInst
	PDEWithdrawals   []*PDEWithdrawalInst
	BeaconTimeStamp  uint64
}

type PDEExtractedInstsRes struct {
	RPCBaseRes
	Result *PDEInfoFromBeaconBlock
}
