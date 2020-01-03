package agents

import (
	"errors"
	"fmt"
	"github.com/incognitochain/incognito-analytic/incognito-data-collector/entities"
	"github.com/incognitochain/incognito-analytic/incognito-data-collector/models"
	"github.com/incognitochain/incognito-analytic/incognito-data-collector/utils"
	"time"
)

const (
	BCHeightStartForPullingPDEState = 49650
)

type PDEStateStore interface {
	GetLatestProcessedBCHeight() (uint64, error)
	StorePDEPoolPair(*models.PDEPoolPair) error
}

type PDEStatePuller struct {
	AgentAbs
	PDEStateStore PDEStateStore
}

// NewPDEStatePuller initialize PDEStatePuller instance
func NewPDEStatePuller(
	name string,
	frequency int,
	rpcClient *utils.HttpClient,
	pdeStateStore PDEStateStore,
) *PDEStatePuller {
	pdeStatePuller := &PDEStatePuller{}
	pdeStatePuller.Name = name
	pdeStatePuller.Frequency = frequency
	pdeStatePuller.Quit = make(chan bool)
	pdeStatePuller.RPCClient = rpcClient
	pdeStatePuller.PDEStateStore = pdeStateStore
	return pdeStatePuller
}

func (psp *PDEStatePuller) getPDEState(beaconHeight uint64) (*entities.PDEState, error) {
	params := []interface{}{
		map[string]interface{}{
			"BeaconHeight": beaconHeight,
		},
	}
	var pdeStateRes entities.PDEStateRes
	err := psp.RPCClient.RPCCall("getpdestate", params, &pdeStateRes)
	if err != nil {
		return nil, err
	}
	if pdeStateRes.RPCError != nil {
		return nil, errors.New(pdeStateRes.RPCError.Message)
	}
	return pdeStateRes.Result, nil
}

// Execute is to pull pde state from incognito chain and put into db
func (psp *PDEStatePuller) Execute() {
	fmt.Println("PDE State Puller agent is executing...")
	// return

	bcHeight, err := psp.PDEStateStore.GetLatestProcessedBCHeight()
	if err != nil {
		fmt.Printf("[PDE State] An error occured while getting the latest processed beacon height: %+v \n", err)
		return
	}
	if bcHeight == 0 {
		bcHeight = uint64(BCHeightStartForPullingPDEState)
	} else {
		bcHeight++
	}

	var lastPDEState *entities.PDEState
	for {
		fmt.Printf("[PDE State] Proccessing for beacon height: %d\n", bcHeight)
		time.Sleep(5 * time.Second)
		pdeState, err := psp.getPDEState(bcHeight)
		if err != nil {
			fmt.Println("An error occured while getting pde state from chain: ", err)
			return
		}

		if pdeState == nil || (lastPDEState != nil && len(lastPDEState.PDEPoolPairs) > 0 && len(pdeState.PDEPoolPairs) == 0) {
			break
		}
		lastPDEState = pdeState
		for _, poolPair := range pdeState.PDEPoolPairs {
			time.Sleep(500 * time.Millisecond)
			poolPairModel := models.PDEPoolPair{
				Token1IDStr:     poolPair.Token1IDStr,
				Token1PoolValue: poolPair.Token1PoolValue,
				Token2IDStr:     poolPair.Token2IDStr,
				Token2PoolValue: poolPair.Token2PoolValue,
				BeaconHeight:    bcHeight,
				BeaconTimeStamp: time.Unix(pdeState.BeaconTimeStamp, 0),
			}
			//fmt.Println(poolPairModel.BeaconTimeStamp.Format("2006-01-02 15:04:05"))
			err := psp.PDEStateStore.StorePDEPoolPair(&poolPairModel)
			if err != nil {
				fmt.Println("An error occured while storing pde pool pair")
				continue
			}
		}
		bcHeight++
	}
	fmt.Println("PDE State Puller agent is finished...")
}
