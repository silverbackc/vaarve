top_markets_query = """
    query TopMarkets($first: Int!) {
        markets(first: $first, orderBy: totalDepositBalanceUSD, orderDirection: desc) {
            totalDepositBalanceUSD
            inputToken {
                symbol
            }
        }
    }
"""