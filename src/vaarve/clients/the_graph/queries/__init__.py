from .markets import top_markets_query
from .borrows import top_borrows_query, top_deposits_query, top_borrows_with_collateral_query, top_two_accounts_query, deposits_query

queries = {
    "top_markets": top_markets_query,
    "top_borrows": top_borrows_query,
    "top_borrows_with_collateral": top_borrows_with_collateral_query,
    "top_deposits": top_deposits_query,
    "top_two_accounts": top_two_accounts_query,
    "deposits": deposits_query,
}