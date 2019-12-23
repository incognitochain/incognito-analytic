package agents

import (
	"encoding/json"
	"errors"
	"fmt"
	"time"

	"github.com/incognitochain/incognito-analytic/pdex-data-collector/entities"
	"github.com/incognitochain/incognito-analytic/pdex-data-collector/models"
	"github.com/incognitochain/incognito-analytic/pdex-data-collector/utils"
)

type ShardBlockStore interface {
	GetLatestProcessedBCHeight(shardID int) (uint64, error)
	StoreShardBloc(block *models.ShardBlock) error
}

type ShardBlockPuller struct {
	AgentAbs
	ShardBlockStore ShardBlockStore
	ShardID         int
}

func NewShardBlockPuller(name string,
	frequency int,
	rpcClient *utils.HttpClient,
	shardID int,
	shardblockStore ShardBlockStore) *ShardBlockPuller {
	puller := &ShardBlockPuller{
		ShardBlockStore: shardblockStore,
		ShardID:         shardID,
		AgentAbs: AgentAbs{
			Name:      name,
			RPCClient: rpcClient,
			Quit:      make(chan bool),
			Frequency: frequency,
		},
	}
	return puller
}

func (puller *ShardBlockPuller) getShardBlock(shardBlockHeight uint64, shardID int) (*entities.ShardBlock, error) {
	params := []interface{}{shardBlockHeight, shardID, "2"}
	var shardBlockRes entities.ShardBlockRes
	err := puller.RPCClient.RPCCall("retrieveblockbyheight", params, &shardBlockRes)
	if err != nil {
		return nil, err
	}
	if shardBlockRes.RPCError != nil {
		return nil, errors.New(shardBlockRes.RPCError.Message)
	}
	return shardBlockRes.Result, nil
}

func (puller *ShardBlockPuller) Execute() {
	fmt.Println("[Shard block puller] Agent is executing...")

	bcHeight, err := puller.ShardBlockStore.GetLatestProcessedBCHeight(puller.ShardID)
	if err != nil {
		fmt.Printf("[Shard block puller] An error occured while getting the latest processed beacon height: %+v \n", err)
		return
	}
	if bcHeight == 0 {
		bcHeight = uint64(1)
	} else {
		bcHeight++
	}

	for {
		fmt.Printf("[Shard block puller] Proccessing for beacon height: %d\n", bcHeight)
		time.Sleep(time.Duration(500) * time.Millisecond)
		shardBlockRes, err := puller.getShardBlock(bcHeight, puller.ShardID)
		if err != nil {
			fmt.Println("[Shard block puller] An error occured while getting pde state from chain: ", err)
			return
		}

		if shardBlockRes == nil {
			break
		}

		shardBlockModel := models.ShardBlock{
			BlockHash:        shardBlockRes.Hash,
			BlockHeight:      shardBlockRes.Height,
			BlockVersion:     shardBlockRes.Version,
			CreatedTime:      time.Unix(shardBlockRes.Time, 0),
			Epoch:            shardBlockRes.Epoch,
			NextBlock:        shardBlockRes.NextBlockHash,
			PreBlock:         shardBlockRes.PreviousBlockHash,
			BeaconBlockHeigh: shardBlockRes.BeaconHeight,
			BlockProducer:    shardBlockRes.BlockProducer,
			CountTx:          len(shardBlockRes.TxHashes),
			ShardID:          puller.ShardID,
			Round:            shardBlockRes.Round,
		}

		dataJson, err1 := json.Marshal(shardBlockRes)
		if err1 == nil {
			shardBlockModel.Data = string(dataJson)
		}
		listTxsJson, err1 := json.Marshal(shardBlockRes.TxHashes)
		if err1 == nil {
			shardBlockModel.ListHashTx = string(listTxsJson)
		}

		err = puller.ShardBlockStore.StoreShardBloc(&shardBlockModel)
		if err != nil {
			fmt.Println("[Shard block puller] An error occured while storing beacon block", err)
			continue
		}
		bcHeight++
	}

	fmt.Println("[Shard block puller] Agent is finished...")
}
