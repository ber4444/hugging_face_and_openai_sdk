# Crypto Price MCP

Add to `.vscode/mcp.json`:

```
{
	"servers": {
		"binance-mcp": {
			"command": "/FULL_PATH_GOES_HERE/.venv/bin/python",
			"args": [
				"/FULL_PATH_GOES_HERE/binance_mcp.py"
			]
		}
	},
	"inputs": []
}
```

Then start the MCP server (inline icon), and you'll be able to type `/mcp.binance-mcp.crypto_summary ETHUSDT` and see a reply like this:

```
ETHUSDT summary:

Price: 1821.14 USDT
24h change: -293.80 USDT (-13.827%)
24h range: 1818.18 → 2173.77 USDT
24h volume: 1,900,168.53 ETH (quote 3,816,897,901.84 USDT)
Want a different symbol or a longer lookback (7d, 30d)?
```