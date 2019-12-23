package pricecalculator

import (
	"fmt"
	"math/big"
	"sort"
)

var (
	PDEPoolPrefix = []byte("pdepool-")
)

const (
	MaxPaths = 20
)

type PriceCalculator struct {
	PairsGraph map[string][]PoolInfo
}

type Pair struct {
	Token1IDStr     string
	Token1PoolValue uint64
	Token2IDStr     string
	Token2PoolValue uint64
}

type PoolInfo struct {
	TokenIDStr     string
	TokenPoolValue uint64
}

func addEdge(
	tokenIDStrSource string,
	tokenIDStrDest string,
	tokentPoolValueDest uint64,
	pairsGraph map[string][]PoolInfo,
) {
	poolInfoDest := PoolInfo{
		TokenIDStr:     tokenIDStrDest,
		TokenPoolValue: tokentPoolValueDest,
	}
	_, found := pairsGraph[tokenIDStrSource]
	if !found {
		pairsGraph[tokenIDStrSource] = []PoolInfo{poolInfoDest}
	} else {
		pairsGraph[tokenIDStrSource] = append(pairsGraph[tokenIDStrSource], poolInfoDest)
	}
}

// NOTEs: the built graph would be undirected graph
func (pc *PriceCalculator) buildPairsGraph(
	pdePoolPairs map[string]Pair,
) {
	pc.PairsGraph = make(map[string][]PoolInfo)
	for _, pair := range pdePoolPairs {
		addEdge(
			pair.Token1IDStr,
			pair.Token2IDStr,
			pair.Token2PoolValue,
			pc.PairsGraph,
		)
		addEdge(
			pair.Token2IDStr,
			pair.Token1IDStr,
			pair.Token1PoolValue,
			pc.PairsGraph,
		)
	}
}

func (pc *PriceCalculator) findPath(
	tokenIDStrSource string,
	tokenIDStrDest string,
	visited map[string]bool,
	path []string,
	allPaths [][]string,
) [][]string {
	if MaxPaths != -1 && len(allPaths) == MaxPaths {
		return allPaths
	}
	path = append(path, tokenIDStrSource)
	visited[tokenIDStrSource] = true

	if tokenIDStrSource == tokenIDStrDest {
		allPaths = append(allPaths, path[:])
	} else {
		poolInfos, found := pc.PairsGraph[tokenIDStrSource]
		if found {
			for _, poolInfo := range poolInfos {
				if visited[poolInfo.TokenIDStr] {
					continue
				}
				allPaths = pc.findPath(poolInfo.TokenIDStr, tokenIDStrDest, visited, path, allPaths)
			}
		}
	}
	path = path[:len(path)-1]
	visited[tokenIDStrSource] = false
	return allPaths
}

func (pc *PriceCalculator) findPaths(
	pdePoolPairs map[string]Pair,
	tokenIDStrSource string,
	tokenIDStrDest string,
) [][]string {
	pc.buildPairsGraph(pdePoolPairs)

	visited := make(map[string]bool)
	for tokenIDStr := range pc.PairsGraph {
		visited[tokenIDStr] = false
	}
	path := []string{}
	allPaths := [][]string{}
	return pc.findPath(
		tokenIDStrSource,
		tokenIDStrDest,
		visited,
		path,
		allPaths,
	)
}

func trade(
	pdePoolPair Pair,
	tokenIDToBuyStr string,
	tokenIDToSellStr string,
	sellAmount uint64,
) uint64 {
	tokenPoolValueToBuy := pdePoolPair.Token1PoolValue
	tokenPoolValueToSell := pdePoolPair.Token2PoolValue
	if pdePoolPair.Token1IDStr == tokenIDToSellStr {
		tokenPoolValueToSell = pdePoolPair.Token1PoolValue
		tokenPoolValueToBuy = pdePoolPair.Token2PoolValue
	}
	invariant := big.NewInt(0)
	invariant.Mul(big.NewInt(int64(tokenPoolValueToSell)), big.NewInt(int64(tokenPoolValueToBuy)))
	newTokenPoolValueToSell := big.NewInt(0)
	newTokenPoolValueToSell.Add(big.NewInt(int64(tokenPoolValueToSell)), big.NewInt(int64(sellAmount)))

	newTokenPoolValueToBuy := big.NewInt(0).Div(invariant, newTokenPoolValueToSell).Uint64()
	modValue := big.NewInt(0).Mod(invariant, newTokenPoolValueToSell)
	if modValue.Cmp(big.NewInt(0)) != 0 {
		newTokenPoolValueToBuy++
	}
	if tokenPoolValueToBuy <= newTokenPoolValueToBuy {
		return 0
	}
	return tokenPoolValueToBuy - newTokenPoolValueToBuy
}

func (pc *PriceCalculator) CalcPrice(
	beaconHeight uint64,
	pdePoolPairs map[string]Pair,
	tokenIDStrSource string,
	tokenIDStrDest string,
) uint64 {
	priceNWeightSum := big.NewInt(0)
	weightSum := big.NewInt(0)
	allPaths := pc.findPaths(pdePoolPairs, tokenIDStrSource, tokenIDStrDest)

	if len(allPaths) == 0 {
		return 0
	}

	for _, path := range allPaths {
		weight := uint64(0)
		sellAmt := uint64(1e9) // hardcoding 1e9 for now, TODO: need to get the right decimal of the source token from db
		for i := 0; i < len(path)-1; i++ {
			tokenIDStrNodeSource := path[i]
			tokenIDStrNodeDest := path[i+1]

			beaconHeightBytes := []byte(fmt.Sprintf("%d-", beaconHeight))
			pdePoolForPairByBCHeightPrefix := append(PDEPoolPrefix, beaconHeightBytes...)
			tokenIDStrs := []string{tokenIDStrNodeSource, tokenIDStrNodeDest}
			sort.Strings(tokenIDStrs)
			poolPairKey := string(append(pdePoolForPairByBCHeightPrefix, []byte(tokenIDStrs[0]+"-"+tokenIDStrs[1])...))

			poolPair, found := pdePoolPairs[poolPairKey]
			if !found || (poolPair.Token1PoolValue == 0 || poolPair.Token2PoolValue == 0) {
				break
			}

			if tokenIDStrNodeSource == tokenIDStrSource {
				if poolPair.Token1IDStr == tokenIDStrSource {
					weight = poolPair.Token1PoolValue
				} else {
					weight = poolPair.Token2PoolValue
				}
			}
			sellAmt = trade(
				poolPair,
				tokenIDStrNodeDest,
				tokenIDStrNodeSource,
				sellAmt,
			)
			if tokenIDStrNodeDest == tokenIDStrDest {
				priceNWeight := big.NewInt(0)
				priceNWeight.Mul(big.NewInt(int64(sellAmt)), big.NewInt(int64(weight)))
				priceNWeightSum.Add(priceNWeightSum, priceNWeight)
				weightSum.Add(weightSum, big.NewInt(int64(weight)))
				break
			}
		}
	}
	if weightSum.Uint64() == 0 {
		return 0
	}
	return priceNWeightSum.Div(priceNWeightSum, weightSum).Uint64()
}
