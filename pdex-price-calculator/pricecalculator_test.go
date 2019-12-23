package pricecalculator

import (
	"testing"
)

func TestCalcPrice(t *testing.T) {
	pc := &PriceCalculator{
		PairsGraph: make(map[string][]PoolInfo),
	}
	beaconHeight := uint64(112656)
	pdePoolPairs := map[string]Pair{
		"pdepool-112656-btc-prv": Pair{
			Token1IDStr:     "prv",
			Token1PoolValue: 1000,
			Token2IDStr:     "btc",
			Token2PoolValue: 200,
		},
		"pdepool-112656-prv-usdt": Pair{
			Token1IDStr:     "prv",
			Token1PoolValue: 3000,
			Token2IDStr:     "usdt",
			Token2PoolValue: 2000,
		},
		"pdepool-112656-btc-usdt": Pair{
			Token1IDStr:     "btc",
			Token1PoolValue: 500,
			Token2IDStr:     "usdt",
			Token2PoolValue: 8000,
		},
	}
	actualPrice := pc.CalcPrice(beaconHeight, pdePoolPairs, "prv", "usdt")
	// prvUsdtPrice := 2000 - (2000 * 3000 / (3000 + 1e9))
	// prvBtcPrice := 200 - (200 * 1000 / (1000 + 1e9)))
	// btcUsdtPrice := 8000 - (8000 * 500 / (500 + prvBtcPrice))
	// expectedPrice := (prvUsdtPrice*3000 + btcUsdtPrice*1000) / (3000 + 1000)
	expectedPrice := uint64(2068)
	if expectedPrice != actualPrice {
		t.Errorf("Calculate price incorrectly, got: %d, want: %d.", actualPrice, expectedPrice)
	}
}
