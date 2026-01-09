markets_query = """
query Markets($request: MarketsRequest!) {
  markets(request: $request) {
    name
    totalMarketSize
    totalAvailableLiquidity
    reserves {
      underlyingToken {
        symbol
      }
      size {
        usdPerToken
        amount {
          value
        }
        usd
      }
    }
  }
}
"""

markets_variables = {
  "request": {
    "chainIds": [1]
  }
}