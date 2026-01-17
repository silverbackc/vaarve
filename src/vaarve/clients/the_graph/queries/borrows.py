top_borrows_query = """
        query TopBorrows($first: Int!) {
        borrows(
            first: $first
            orderBy: amountUSD
            orderDirection: desc
            where: {position_: {blockNumberClosed: null}}
        ) {
            id
            amountUSD
            asset {
              symbol
            }
            account {
              id
            }
        }
        }
"""

top_deposits_query = """
        query TopDeposits($first: Int!) {
          deposits(
              first: $first
              orderBy: amountUSD
              orderDirection: desc
              where: {position_: {blockNumberClosed: null}}
          ) {
              amountUSD
              asset {
                symbol
              }
              account {
                id
              }
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
      deposits(
        first: $first
        where: {position_: {blockNumberClosed: null}},
        orderBy: amountUSD
        orderDirection: desc
      ) {
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

deposits_query = """
query Deposits($first: Int!, $account_ids: [String!]) {
  deposits(
    first: $first
    where: {account_: {id_in: $account_ids}, position_: {blockNumberClosed: null}}
    orderBy: amountUSD
    orderDirection: desc
  ) {
    amountUSD
    amount
    asset {
      symbol
      decimals
    }
    account {
      id
    }
  }
}
"""

top_two_accounts_query = """
query MyQuery {
  accounts(
    where: {id_in: ["0x9600a48ed0f931d0c422d574e3275a90d8b22745", "0xf0bb20865277abd641a307ece5ee04e79073416c"]}
  ) {
    id
    positions {
      borrowCount
      depositCount
      borrows(where: {position_: {blockNumberClosed: null}}) {
        amountUSD
      }
      deposits(where: {position_: {blockNumberClosed: null}}) {
        amountUSD
      }
    }
  }
}
"""