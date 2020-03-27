package agents

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"time"

	"github.com/incognitochain/incognito-analytic/incognito-data-collector/entities"
	"github.com/incognitochain/incognito-analytic/incognito-data-collector/models"
	"github.com/incognitochain/incognito-analytic/incognito-data-collector/utils"
)

type ShardBlockStore interface {
	GetLatestProcessedShardHeight(shardID int) (uint64, error)
	StoreShardBlock(block *models.ShardBlock) error
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
	return shardBlockRes.Result[0], nil
}

func (puller *ShardBlockPuller) Execute() {
	fmt.Println("[Shard block puller] Agent is executing...")

	blockHeight, err := puller.ShardBlockStore.GetLatestProcessedShardHeight(puller.ShardID)
	if err != nil {
		log.Printf("[Shard block puller] An error occured while getting the latest processed shard block height: %+v \n", err)
		return
	}
	if blockHeight == 0 {
		blockHeight = uint64(1)
	} else {
		blockHeight++
	}

	for {
		log.Printf("[Shard block puller] Proccessing for shard %d block height: %d\n", puller.ShardID, blockHeight)
		time.Sleep(500 * time.Millisecond)
		shardBlockRes, err := puller.getShardBlock(blockHeight, puller.ShardID)
		if err != nil {
			log.Printf("[Shard block puller] An error occured while getting shard %d block height %d from chain: %+v \n", puller.ShardID, blockHeight, err)
			continue
		}

		if shardBlockRes == nil {
			break
		}

		blockHeightTemp, _ := puller.ShardBlockStore.GetLatestProcessedShardHeight(puller.ShardID)
		if blockHeightTemp == shardBlockRes.Height {
			continue
		}

		if shardBlockRes.NextBlockHash == "" {
			continue
		}

		shardBlockModel := models.ShardBlock{
			BlockHash:         shardBlockRes.Hash,
			BlockHeight:       shardBlockRes.Height,
			BlockVersion:      shardBlockRes.Version,
			CreatedTime:       time.Unix(shardBlockRes.Time, 0),
			Epoch:             shardBlockRes.Epoch,
			NextBlock:         shardBlockRes.NextBlockHash,
			PreBlock:          shardBlockRes.PreviousBlockHash,
			BeaconBlockHeight: shardBlockRes.BeaconHeight,
			BlockProducer:     shardBlockRes.BlockProducer,
			CountTx:           len(shardBlockRes.TxHashes),
			ShardID:           puller.ShardID,
			Round:             shardBlockRes.Round,
		}

		dataJson, err1 := json.Marshal(shardBlockRes)
		if err1 == nil {
			shardBlockModel.Data = string(dataJson)
		}
		if len(shardBlockRes.Txs) > 0 {
			listTx := []string{}
			for _, tx := range shardBlockRes.Txs {
				listTx = append(listTx, tx.Hash)
			}
			listTxsJson, err1 := json.Marshal(listTx)
			if err1 == nil {
				shardBlockModel.ListHashTx = string(listTxsJson)
			}
		} else {
			shardBlockModel.ListHashTx = "[]"
		}

		err = puller.ShardBlockStore.StoreShardBlock(&shardBlockModel)
		if err != nil {
			log.Printf("[Shard block puller] An error occured while storing shard block %d, shard %d err: %+v\n", blockHeight, puller.ShardID, err)
			continue
		}
		blockHeight++
	}

	log.Println("[Shard block puller] Agent is finished...")
}
