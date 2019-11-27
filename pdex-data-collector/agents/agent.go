package agents

import (
	"fmt"
	"pdex-data-collector/utils"
)

type AgentAbs struct {
	Name      string
	Frequency int // in sec
	Quit      chan bool
	RPCClient *utils.HttpClient
}

type Agent interface {
	Execute()
	GetName() string
	GetFrequency() int
	GetQuitChan() chan bool
}

func (a *AgentAbs) Execute() {
	fmt.Println("Abstract agent is executing...")
}

func (a *AgentAbs) GetName() string {
	return a.Name
}

func (a *AgentAbs) GetFrequency() int {
	return a.Frequency
}

func (a *AgentAbs) GetQuitChan() chan bool {
	return a.Quit
}
