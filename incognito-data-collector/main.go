package main

import (
	"fmt"
	"github.com/incognitochain/incognito-analytic/incognito-data-collector/agents"
	pg "github.com/incognitochain/incognito-analytic/incognito-data-collector/databases/postgresql"
	"github.com/incognitochain/incognito-analytic/incognito-data-collector/utils"
	"log"
	"os"
	"os/signal"
	"runtime"
	"strconv"
	"syscall"
	"time"
)

// Server info struct
type Server struct {
	quit   chan os.Signal
	finish chan bool
	agents []agents.Agent
}

func registerPDEStatePuller(
	rpcClient *utils.HttpClient,
	agentsList []agents.Agent,
	pdeStateStore *pg.PDEStatePGStore,
) []agents.Agent {
	pdeStatePuller := agents.NewPDEStatePuller(
		"PDE-State-Puller",
		3, // in sec
		rpcClient,
		pdeStateStore,
	)
	return append(agentsList, pdeStatePuller)
}

func registerPDEInstsExtractor(
	rpcClient *utils.HttpClient,
	agentsList []agents.Agent,
	pdeInstructionsPGStore *pg.PDEInstructionsPGStore,
) []agents.Agent {
	pdeStatePuller := agents.NewPDEInstsExtractor(
		"PDE-Instructions-Extractor",
		3, // in sec
		rpcClient,
		pdeInstructionsPGStore,
	)
	return append(agentsList, pdeStatePuller)
}

func registerBeaconBlockPuller(
	rpcClient *utils.HttpClient,
	agentsList []agents.Agent,
	beaconBlockStore *pg.BeaconBlockStore,
) []agents.Agent {
	pdeStatePuller := agents.NewBeaconBlockPuller(
		"Beacon-Block-Puller",
		3, // in sec
		rpcClient,
		beaconBlockStore,
	)
	return append(agentsList, pdeStatePuller)
}

func registerShardBlockPuller(
	shardID int,
	rpcClient *utils.HttpClient,
	agentsList []agents.Agent,
	shardBlockStore *pg.ShardBlockStore,
) []agents.Agent {
	shardBlockPuller := agents.NewShardBlockPuller(
		"Shard-Block-Puller-Shard-"+strconv.Itoa(shardID),
		3, // in sec
		rpcClient,
		shardID,
		shardBlockStore,
	)
	return append(agentsList, shardBlockPuller)
}

func registerTransactionPuller(
	shardID int,
	rpcClient *utils.HttpClient,
	agentsList []agents.Agent,
	transactionsStore *pg.TransactionsStore,
) []agents.Agent {
	txPuller := agents.NewTransactionPuller(
		"Transaction-Puller-Shard-"+strconv.Itoa(shardID),
		3, // in sec
		rpcClient,
		shardID,
		transactionsStore,
	)
	return append(agentsList, txPuller)
}

func registerTokenPuller(
	rpcClient *utils.HttpClient,
	agentsList []agents.Agent,
	tokenStore *pg.TokensStore,
) []agents.Agent {
	tokenPuller := agents.NewTokenPuller(
		"Token-Puller",
		3, // in sec
		rpcClient,
		tokenStore,
	)
	return append(agentsList, tokenPuller)
}

// NewServer is to new server instance
func NewServer() (*Server, error) {
	rpcClient := utils.NewHttpClient()
	agentsList := []agents.Agent{}

	// ----------------------- Register agent -----------------------
	// pde instruction
	pdeStateStore, err := pg.NewPDEStatePGStore()
	if err != nil {
		return nil, err
	}
	agentsList = registerPDEStatePuller(rpcClient, agentsList, pdeStateStore)

	// pde instruction
	pdeInstructionsPGStore, err := pg.NewPDEInstructionsPGStore()
	if err != nil {
		return nil, err
	}
	agentsList = registerPDEInstsExtractor(rpcClient, agentsList, pdeInstructionsPGStore)

	// beacon block
	beaconBlockStore, err := pg.NewBeaconBlockStore()
	if err != nil {
		return nil, err
	}
	agentsList = registerBeaconBlockPuller(rpcClient, agentsList, beaconBlockStore)

	// shard block: 8 shard
	shardBlockStore, err := pg.NewShardBlockStore()
	if err != nil {
		return nil, err
	}
	for i := 0; i <= 7; i++ {
		agentsList = registerShardBlockPuller(i, rpcClient, agentsList, shardBlockStore)
	}

	// tx: 8 shard
	txStore, err := pg.NewTransactionsStore()
	if err != nil {
		return nil, err
	}
	for i := 0; i <= 7; i++ {
		agentsList = registerTransactionPuller(i, rpcClient, agentsList, txStore)
	}

	// Token
	tokenStore, err := pg.NewTokensStore()
	if err != nil {
		return nil, err
	}
	agentsList = registerTokenPuller(rpcClient, agentsList, tokenStore)

	//
	// ----------------------- End -----------------------

	quitChan := make(chan os.Signal)
	signal.Notify(quitChan, syscall.SIGTERM)
	signal.Notify(quitChan, syscall.SIGINT)
	return &Server{
		quit:   quitChan,
		finish: make(chan bool, len(agentsList)),
		agents: agentsList,
	}, nil
}

// NotifyQuitSignal is to listen quit signals on quit channel
// and notify the signal to every registered agennt
func (s *Server) NotifyQuitSignal(agents []agents.Agent) {
	sig := <-s.quit
	fmt.Printf("Caught sig: %+v \n", sig)
	// notify all agents about quit signal
	for _, a := range agents {
		a.GetQuitChan() <- true
	}
}

// Run is to start executing registered agents
func (s *Server) Run() {
	agents := s.agents
	go s.NotifyQuitSignal(agents)
	for _, a := range agents {
		go executeAgent(s.finish, a)
	}
}

func executeAgent(
	finish chan bool,
	agent agents.Agent,
) {
	agent.Execute() // execute as soon as starting up
	for {
		select {
		case <-agent.GetQuitChan():
			fmt.Printf("Finishing task for %s ...\n", agent.GetName())
			time.Sleep(time.Second * 1)
			fmt.Printf("Task for %s done! \n", agent.GetName())
			finish <- true
			break
		case <-time.After(time.Duration(agent.GetFrequency()) * time.Second):
			agent.Execute()
		}
	}
}

func main() {
	log.SetOutput(os.Stdout)
	runtime.GOMAXPROCS(runtime.NumCPU())
	s, err := NewServer()
	if err != nil {
		return
	}
	s.Run()
	for range s.agents {
		<-s.finish
	}
	fmt.Println("Server stopped gracefully!")
}
