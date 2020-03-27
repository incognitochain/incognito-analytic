package entities

type BeaconBlock struct {
	Hash              string     `json:"Hash"`
	Height            uint64     `json:"Height"`
	BlockProducer     string     `json:"BlockProducer"`
	ValidationData    string     `json:"ValidationData"`
	ConsensusType     string     `json:"ConsensusType"`
	Version           int        `json:"Version"`
	Epoch             uint64     `json:"Epoch"`
	Round             int        `json:"Round"`
	Time              int64      `json:"Time"`
	PreviousBlockHash string     `json:"PreviousBlockHash"`
	NextBlockHash     string     `json:"NextBlockHash"`
	Instructions      [][]string `json:"Instructions"`
	Size              uint64     `json:"Size"`
}

type BeaconBlockRes struct {
	RPCBaseRes
	Result []*BeaconBlock
}
