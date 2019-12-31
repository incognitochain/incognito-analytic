package postgresql

import (
	"fmt"
	"os"

	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
)

const (
	userName = ""
	password = ""
	dbName   = "pdex"
	host     = "127.0.0.1"
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
	userNameP := os.Getenv("postgresuser")
	if userNameP == "" {
		userNameP = userName
	}
	passwordP := os.Getenv("postgrespwd")
	if passwordP == "" {
		passwordP = password
	}
	hostP := os.Getenv("postgreshost")
	if hostP == "" {
		hostP = host
	}
	portP := os.Getenv("postgresport")
	if portP == "" {
		portP = port
	}
	dbNameP := os.Getenv("postgresdb")
	if dbNameP == "" {
		dbNameP = dbName
	}
	connStr := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable", userNameP, passwordP, hostP, portP, dbNameP)
	pgConn, err := sqlx.Open("postgres", connStr)
	if err != nil {
		fmt.Println("An error occured while openning connection to pg")
		return nil, err
	}
	return pgConn, nil
}
