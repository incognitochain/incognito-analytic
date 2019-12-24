package postgresql

import "github.com/incognitochain/incognito-analytic/incognito-data-collector/models"

type TokensStore struct {
	PGStoreAbs
}

func NewTokensStore() (*TokensStore, error) {
	pgConn, err := getPGConnection()
	if err != nil {
		return nil, err
	}
	store := &TokensStore{}
	store.DB = pgConn
	return store, nil
}

func (st *TokensStore) GetListTokenIds() ([]string, error) {
	sql := `
		SELECT token_id FROM tokens
	`
	result := []string{}
	err := st.DB.Select(&result, sql)
	if err != nil {
		return nil, err
	}
	return result, nil
}

func (st *TokensStore) StoreToken(token *models.Token) error {
	sqlStr := `
		INSERT INTO tokens (token_id, name, symbol, supply, info, data)
		VALUES (:token_id, :name, :symbol, :supply, :info, :data)
		RETURNING id
	`
	tx := st.DB.MustBegin()
	defer tx.Commit()
	_, err := tx.NamedQuery(sqlStr, token)
	return err
}

func (st *TokensStore) UpdateToken(token *models.Token) error {
	sqlStr := `
		UPDATE tokens SET count_tx=$1, list_hash_tx=$2 WHERE token_id=$3
		RETURNING id
	`
	tx := st.DB.MustBegin()
	defer tx.Commit()
	_, err := tx.Exec(sqlStr, token.CountTx, token.ListHashTx, token.TokenID)
	return err
}
