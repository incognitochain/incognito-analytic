package entities

type ShardBlock struct {
	Hash              string               `json:"Hash"`
	ShardID           byte                 `json:"ShardID"`
	Height            uint64               `json:"Height"`
	Confirmations     int64                `json:"Confirmations"`
	Version           int                  `json:"Version"`
	TxRoot            string               `json:"TxRoot"`
	Time              int64                `json:"Time"`
	PreviousBlockHash string               `json:"PreviousBlockHash"`
	NextBlockHash     string               `json:"NextBlockHash"`
	TxHashes          []string             `json:"TxHashes"`
	Txs               []ShardBlockTxResult `json:"Txs"`
	BlockProducer     string               `json:"BlockProducer"`
	ValidationData    string               `json:"ValidationData"`
	ConsensusType     string               `json:"ConsensusType"`
	Data              string               `json:"Data"`
	BeaconHeight      uint64               `json:"BeaconHeight"`
	BeaconBlockHash   string               `json:"BeaconBlockHash"`
	Round             int                  `json:"Round"`
	Epoch             uint64               `json:"Epoch"`
	Reward            uint64               `json:"Reward"`
	RewardBeacon      uint64               `json:"RewardBeacon"`
	Fee               uint64               `json:"Fee"`
	Size              uint64               `json:"Size"`
	Instruction       [][]string           `json:"Instruction"`
	CrossShardBitMap  []int                `json:"CrossShardBitMap"`
}

type ShardBlockTxResult struct {
	Hash     string `json:"Hash"`
	Locktime int64  `json:"Locktime"`
	HexData  string `json:"HexData"`
}

type ShardBlockRes struct {
	RPCBaseRes
	Result []*ShardBlock
}
