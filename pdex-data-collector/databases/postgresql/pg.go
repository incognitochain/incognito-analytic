package postgresql

import (
	"fmt"

	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
)

const (
	userName = "postgres"
	password = "postgres"
	dbName   = "pdex"
	host     = "34.94.185.164"
	port     = "5432"
)

// PGStoreAbs is PDE State postgresql store abstraction
type PGStoreAbs struct {
	DB *sqlx.DB
}

// TODO: ensure pdex db exist.

var pgConn *sqlx.DB

func getPGConnection() (*sqlx.DB, error) {
	if pgConn != nil {
		return pgConn, nil
	}
	connStr := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable", userName, password, host, port, dbName)
	pgConn, err := sqlx.Open("postgres", connStr)
	if err != nil {
		fmt.Println("An error occured while openning connection to pg")
		return nil, err
	}
	return pgConn, nil
}
