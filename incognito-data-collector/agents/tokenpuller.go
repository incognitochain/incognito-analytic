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

type TokenStore interface {
	GetListTokenIds() ([]string, error)
	StoreToken(token *models.Token) error
	UpdateToken(token *models.Token) error
}

type TokenPuller struct {
	AgentAbs
	TokenStore TokenStore
}

func NewTokenPuller(name string,
	frequency int,
	rpcClient *utils.HttpClient,
	tokenStore TokenStore) *TokenPuller {
	puller := &TokenPuller{
		TokenStore: tokenStore,
		AgentAbs: AgentAbs{
			Name:      name,
			RPCClient: rpcClient,
			Quit:      make(chan bool),
			Frequency: frequency,
		},
	}
	return puller
}

func (puller *TokenPuller) getListToken() (*entities.ListCustomToken, error) {
	params := []interface{}{}
	var listTokenRes entities.ListCustomTokenRes
	err := puller.RPCClient.RPCCall("listprivacycustomtoken", params, &listTokenRes)
	if err != nil {
		return nil, err
	}
	if listTokenRes.RPCError != nil {
		return nil, errors.New(listTokenRes.RPCError.Message)
	}
	return listTokenRes.Result, nil
}

func (puller *TokenPuller) getToken(tokenID string) (*entities.CustomToken, error) {
	params := []interface{}{tokenID}
	var listTokenRes entities.CustomTokenRes
	err := puller.RPCClient.RPCCall("privacycustomtoken", params, &listTokenRes)
	if err != nil {
		return nil, err
	}
	if listTokenRes.RPCError != nil {
		return nil, errors.New(listTokenRes.RPCError.Message)
	}
	return listTokenRes.Result, nil
}

func (puller *TokenPuller) Execute() {
	fmt.Println("[Token puller] Agent is executing...")

	for {
		currentTokens, err := puller.TokenStore.GetListTokenIds()
		if err != nil {
			return
		}

		listTokensOnChain, err := puller.getListToken()
		if err != nil {
			continue
		}

		for _, token := range listTokensOnChain.ListCustomToken {
			if !utils.StringInSlice(token.ID, currentTokens) {
				tokenModel := models.Token{
					Name:    token.Name,
					TokenID: token.ID,
					Symbol:  token.Symbol,
					Supply:  token.Amount,
					Info:    token.TxInfo,
				}

				dataJson, err := json.Marshal(token)
				if err != nil {
					fmt.Printf("[Token puller] An error occured while json.Marshal %s %s: %+v\n", token.ID, token.Name, err)
					continue
				}
				tokenModel.Data = string(dataJson)

				err = puller.TokenStore.StoreToken(&tokenModel)
				if err != nil {
					fmt.Printf("[Token puller] An error occured while StoreToken %s %s: %+v\n", token.ID, token.Name, err)
					continue
				} else {
					fmt.Printf("[Token puller] Add token success %s %s\n", token.ID, token.Name)
				}
			}
		}

		for _, tokenId := range currentTokens {
			token, err := puller.getToken(tokenId)
			if err != nil {
				fmt.Printf("[Token puller] An error occured while getToken by id %s %s\n", token.ID, token.Name, err)
				continue
			}
			tokenModel := models.Token{
				TokenID: token.ID,
				CountTx: len(token.ListTxs),
			}
			if tokenModel.CountTx > 0 {
				jsonListTxs, err := json.Marshal(token.ListTxs)
				if err != nil {
					fmt.Printf("[Token puller] An error occured while json Marshal ListTxs by id %s %s: %+v\n", token.ID, token.Name, err)
					continue
				}
				jsonListTxsStr := string(jsonListTxs)
				tokenModel.ListHashTx = &jsonListTxsStr
			}
			err = puller.TokenStore.UpdateToken(&tokenModel)
			if err != nil {
				fmt.Printf("[Token puller] An error occured while UpdateToken by id %s %s: %+v\n", token.ID, token.Name, err)
				continue
			} else {
				fmt.Printf("[Token puller] Update token success %s %s\n", token.ID, token.Name)
			}
		}
		time.Sleep(30 * time.Second)
	}
}
