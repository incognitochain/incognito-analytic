package entities

type RPCError struct {
	Code    int    `json:"Code"`
	Message string `json:"Message"`
}

type RPCBaseRes struct {
	ID       int       `json:"Id"`
	RPCError *RPCError `json:"Error"`
}
