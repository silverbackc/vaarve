top_borrows_query = """
        query TopBorrows($first: Int!) {
        borrows(
            first: $first
            orderBy: amountUSD
            orderDirection: desc
            where: {position_: {blockNumberClosed: null}}
        ) {
            amountUSD
            asset {
            symbol
            }
            amount
            timestamp
        }
        }
"""

top_borrows_with_collateral_query = """
query TopBorrowsWithDeposits($first: Int!) {
  borrows(
    first: $first
    orderBy: amountUSD
    orderDirection: desc
    where: {position_: {blockNumberClosed: null}}
  ) {
    amount
    amountUSD
    asset {
      symbol
      decimals
    }
    account {
      id
      deposits(where: {position_: {blockNumberClosed: null}}) {
        amountUSD
        amount
        asset {
          symbol
          decimals
        }
        id
      }
    }
  }
}
"""