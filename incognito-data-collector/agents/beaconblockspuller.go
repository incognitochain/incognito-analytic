package agents

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/incognitochain/incognito-analytic/incognito-data-collector/entities"
	"github.com/incognitochain/incognito-analytic/incognito-data-collector/models"
	"github.com/incognitochain/incognito-analytic/incognito-data-collector/utils"
	"time"
)

type BeaconBlockStore interface {
	GetLatestProcessedBCHeight() (uint64, error)
	StoreBeaconBlock(block *models.BeaconBlock) error
}

type BeaconBlockPuller struct {
	AgentAbs
	BeaconBlockStore BeaconBlockStore
}

func NewBeaconBlockPuller(name string,
	frequency int,
	rpcClient *utils.HttpClient,
	beaconblockStore BeaconBlockStore) *BeaconBlockPuller {
	puller := &BeaconBlockPuller{
		BeaconBlockStore: beaconblockStore,
		AgentAbs: AgentAbs{
			Name:      name,
			Frequency: frequency,
			Quit:      make(chan bool),
			RPCClient: rpcClient,
		},
	}
	return puller
}

func (puller *BeaconBlockPuller) getBeaconBlock(beaconHeight uint64) (*entities.BeaconBlock, error) {
	params := []interface{}{beaconHeight}
	var beaconBlock entities.BeaconBlockRes
	err := puller.RPCClient.RPCCall("retrievebeaconblockbyheight", params, &beaconBlock)
	if err != nil {
		return nil, err
	}
	if beaconBlock.RPCError != nil {
		return nil, errors.New(beaconBlock.RPCError.Message)
	}
	return beaconBlock.Result, nil
}

func (puller *BeaconBlockPuller) Execute() {
	fmt.Println("[Beacon block puller] Agent is executing...")

	bcHeight, err := puller.BeaconBlockStore.GetLatestProcessedBCHeight()
	if err != nil {
		fmt.Printf("[Beacon block puller] An error occured while getting the latest processed beacon height: %+v \n", err)
		return
	}
	if bcHeight == 0 {
		bcHeight = uint64(1)
	} else {
		bcHeight++
	}

	for {
		fmt.Printf("[Beacon block puller] Proccessing for beacon height: %d\n", bcHeight)
		time.Sleep(120 * time.Second)
		beaconBlockRes, err := puller.getBeaconBlock(bcHeight)
		if err != nil {
			fmt.Println("[Beacon block puller] An error occured while getting pde state from chain: ", err)
			continue
		}

		if beaconBlockRes == nil {
			continue
		}

		if beaconBlockRes.NextBlockHash == "" {
			continue
		}

		bcHeightTemp, _ := puller.BeaconBlockStore.GetLatestProcessedBCHeight()
		if bcHeightTemp == beaconBlockRes.Height {
			continue
		}

		beaconBlockModel := models.BeaconBlock{
			BlockHash:    beaconBlockRes.Hash,
			BlockHeight:  beaconBlockRes.Height,
			BlockVersion: beaconBlockRes.Version,
			CreatedTime:  time.Unix(beaconBlockRes.Time, 0),
			Epoch:        beaconBlockRes.Epoch,
			NextBlock:    beaconBlockRes.NextBlockHash,
			PreBlock:     beaconBlockRes.PreviousBlockHash,
			Round:        beaconBlockRes.Round,
		}

		dataJson, err1 := json.Marshal(beaconBlockRes)
		if err1 == nil {
			beaconBlockModel.Data = string(dataJson)
		}
		instructionsJson, err1 := json.Marshal(beaconBlockRes.Instructions)
		if err1 == nil {
			beaconBlockModel.Instructions = string(instructionsJson)
		}

		err = puller.BeaconBlockStore.StoreBeaconBlock(&beaconBlockModel)
		if err != nil {
			fmt.Println("[Beacon block puller] An error occured while storing beacon block", err)
			continue
		}
		bcHeight++
	}

	fmt.Println("[Beacon block puller] Agent is finished...")
}
