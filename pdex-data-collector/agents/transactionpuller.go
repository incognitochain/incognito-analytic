package agents

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/incognitochain/incognito-analytic/pdex-data-collector/databases/postgresql"
	"github.com/incognitochain/incognito-analytic/pdex-data-collector/entities"
	"github.com/incognitochain/incognito-analytic/pdex-data-collector/models"
	"github.com/incognitochain/incognito-analytic/pdex-data-collector/utils"
	"time"
)

type TransactionsStore interface {
	GetLatestProcessedShardHeight(shardID int) (uint64, error)
	StoreTransaction(txs *models.Transaction) error
	LatestProcessedTxByHeight(shardID int, blockHeight uint64) ([]string, error)
	ListProcessingTxByHeight(shardID int, blockHeight uint64) (*postgresql.ListProcessingTx, error)
	ListNeedProcessingTxByHeight(shardID int, blockHeight uint64) ([]*postgresql.ListProcessingTx, error)
}

type TransactionPuller struct {
	AgentAbs
	TransactionsStore TransactionsStore
	ShardID           int
}

func NewTransactionPuller(name string,
	frequency int,
	rpcClient *utils.HttpClient,
	shardID int,
	transactionsStore TransactionsStore) *TransactionPuller {
	puller := &TransactionPuller{
		TransactionsStore: transactionsStore,
		ShardID:           shardID,
		AgentAbs: AgentAbs{
			Name:      name,
			RPCClient: rpcClient,
			Quit:      make(chan bool),
			Frequency: frequency,
		},
	}
	return puller
}

func (puller *TransactionPuller) getTransaction(txHash string) (*entities.TransactionDetail, error) {
	params := []interface{}{"txHash"}
	var shardBlockRes entities.TransactionDetailRes
	err := puller.RPCClient.RPCCall("gettransactionbyhash", params, &shardBlockRes)
	if err != nil {
		return nil, err
	}
	if shardBlockRes.RPCError != nil {
		return nil, errors.New(shardBlockRes.RPCError.Message)
	}
	return shardBlockRes.Result, nil
}

func stringInSlice(a string, list []string) bool {
	for _, b := range list {
		if b == a {
			return true
		}
	}
	return false
}

func (puller *TransactionPuller) Execute() {
	fmt.Println("[Transaction puller] Agent is executing...")

	processingTxs := []string{}
	latestBlockHeight, err := puller.TransactionsStore.GetLatestProcessedShardHeight(puller.ShardID)
	if err != nil {
		fmt.Printf("[Transaction puller] An error occured while getting the latest processed shard block height: %+v \n", err)
		return
	}
	if latestBlockHeight > 0 {
		latestTxs, err := puller.TransactionsStore.LatestProcessedTxByHeight(puller.ShardID, latestBlockHeight)
		if err != nil {
			fmt.Printf("[Transaction puller] An error occured while getting the latest processed shard block height: %+v \n", err)
			return
		}

		temp, err := puller.TransactionsStore.ListProcessingTxByHeight(puller.ShardID, latestBlockHeight)
		if err != nil {
			fmt.Printf("[Transaction puller] An error occured while getting the latest processed shard block height: %+v \n", err)
			return
		}

		if len(temp.TxsHash) > len(latestTxs) {
			for _, a := range temp.TxsHash {
				if !stringInSlice(a, latestTxs) {
					processingTxs = append(processingTxs, a)
				}
			}
		}
	} else {
		latestBlockHeight = 0
	}

	latestBlockHeight += 1

	temp, err := puller.TransactionsStore.ListNeedProcessingTxByHeight(puller.ShardID, latestBlockHeight)
	if len(temp) > 0 {
		for _, t := range temp {
			processingTxs = append(processingTxs, t.TxsHash...)
		}
	}

	if len(processingTxs) > 0 {
		for _, t := range processingTxs {
			time.Sleep(time.Duration(500) * time.Millisecond)
			tx, e := puller.getTransaction(t)
			if e != nil {
				fmt.Printf("[Transaction puller] An error occured while getting transaction %s : %+v\n", tx, err)
				return
			}

			txModel := models.Transaction{
				ShardID:     int(tx.ShardID),
				BlockHeight: tx.BlockHeight,
				BlockHash:   tx.BlockHash,
				Info:        tx.Info,
				TxID:        tx.Hash,
				TxType:      tx.Type,
				TxVersion:   tx.Version,
				PRVFee:      tx.Fee,
				//Data:
				Proof: tx.Proof,
				//ProofDetail: tx.ProofDetail
				TransactedPrivacyCoinFee: tx.PrivacyCustomTokenFee,
				TransactedPrivacyCoin:    tx.PrivacyCustomTokenData,
				//TransactedPrivacyCoinProofDetail: tx.PrivacyCustomTokenProofDetail,
			}
			dataJson, err := json.Marshal(tx)
			if err == nil {
				txModel.Data = string(dataJson)
			}
			metadataJson, err := json.Marshal(tx.Metadata)
			if err == nil {
				txModel.Data = string(metadataJson)
			}
			proofDetailJson, err := json.Marshal(tx.ProofDetail)
			if err == nil {
				txModel.ProofDetail = string(proofDetailJson)
			}
			privacyCustomTokenProofDetailJson, err := json.Marshal(tx.PrivacyCustomTokenProofDetail)
			if err == nil {
				txModel.TransactedPrivacyCoinProofDetail = string(privacyCustomTokenProofDetailJson)
			}
			txModel.CreatedTime, _ = time.Parse("2006-01-02T15:04:05.999999", tx.LockTime)
			err = puller.TransactionsStore.StoreTransaction(&txModel)
			if err != nil {
				fmt.Printf("[Transaction puller] An error occured while storing tx %s, shard %d err: %+v\n", t, puller.ShardID, err)
				continue
			}
		}
	}

	fmt.Println("[Transaction puller] Agent is finished...")
}
