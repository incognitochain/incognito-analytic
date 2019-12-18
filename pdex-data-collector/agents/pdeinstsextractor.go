package agents

import (
	"errors"
	"fmt"
	"github.com/incognitochain/incognito-analytic/pdex-data-collector/entities"
	"github.com/incognitochain/incognito-analytic/pdex-data-collector/models"
	"github.com/incognitochain/incognito-analytic/pdex-data-collector/utils"
	"time"
)

const (
	BCHeightStartForExtractingInsts = 49650
)

type PDEInstructionsStore interface {
	GetLatestProcessedBCHeight() (uint64, error)
	StorePDETrade(*models.PDETrade) error
}

type PDEInstsExtractor struct {
	AgentAbs
	PDEInstructionsStore PDEInstructionsStore
}

// NewPDEInstsExtractor instantiates PDEInstsExtractor
func NewPDEInstsExtractor(
	name string,
	frequency int,
	rpcClient *utils.HttpClient,
	pdeInstructionsStore PDEInstructionsStore,
) *PDEInstsExtractor {
	pdeInstsExtractor := &PDEInstsExtractor{}
	pdeInstsExtractor.Name = name
	pdeInstsExtractor.Frequency = frequency
	pdeInstsExtractor.Quit = make(chan bool)
	pdeInstsExtractor.RPCClient = rpcClient
	pdeInstsExtractor.PDEInstructionsStore = pdeInstructionsStore
	return pdeInstsExtractor
}

func (pie *PDEInstsExtractor) extractPDEInstsFromBeaconBlk(beaconHeight uint64) (*entities.PDEInfoFromBeaconBlock, error) {
	params := []interface{}{
		map[string]interface{}{
			"BeaconHeight": beaconHeight,
		},
	}
	var pdeExtractedInstsRes entities.PDEExtractedInstsRes
	err := pie.RPCClient.RPCCall("extractpdeinstsfrombeaconblock", params, &pdeExtractedInstsRes)
	if err != nil {
		return nil, err
	}
	// bb, _ := json.Marshal(pdeExtractedInstsRes)
	// fmt.Println("hahaha: ", string(bb))
	if pdeExtractedInstsRes.RPCError != nil {
		return nil, errors.New(pdeExtractedInstsRes.RPCError.Message)
	}
	return pdeExtractedInstsRes.Result, nil
}

// Execute is to pull pde state from incognito chain and put into db
func (pie *PDEInstsExtractor) Execute() {
	fmt.Println("PDE InstsExtractor agent is executing...")
	// return

	bcHeight, err := pie.PDEInstructionsStore.GetLatestProcessedBCHeight()
	if err != nil {
		fmt.Printf("[Instructions Extractor] An error occured while getting the latest processed beacon height: %+v \n", err)
		return
	}
	if bcHeight == 0 {
		bcHeight = uint64(BCHeightStartForExtractingInsts)
	} else {
		bcHeight++
	}

	for {
		time.Sleep(time.Duration(1000) * time.Millisecond)
		fmt.Printf("[Instructions Extractor] Proccessing for beacon height: %d", bcHeight)
		insts, err := pie.extractPDEInstsFromBeaconBlk(bcHeight)
		if err != nil {
			fmt.Println("An error occured while extracting pde instruction from chain: ", err)
			return
		}
		if insts == nil {
			break
		}
		for _, trade := range insts.PDETrades {
			time.Sleep(time.Duration(200) * time.Millisecond)
			tradeModel := models.PDETrade{
				TraderAddressStr:    trade.TraderAddressStr,
				ReceivingTokenIDStr: trade.ReceivingTokenIDStr,
				ReceiveAmount:       trade.ReceiveAmount,
				Token1IDStr:         trade.Token1IDStr,
				Token2IDStr:         trade.Token2IDStr,
				ShardID:             trade.ShardID,
				RequestedTxID:       trade.RequestedTxID,
				Status:              trade.Status,
				BeaconHeight:        trade.BeaconHeight,
			}
			err := pie.PDEInstructionsStore.StorePDETrade(&tradeModel)
			if err != nil {
				fmt.Println("An error occured while storing pde trade")
				continue
			}
		}
		bcHeight++
	}
	fmt.Println("PDE InstsExtractor agent is finished...")
}
