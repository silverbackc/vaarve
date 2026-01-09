from .markets import top_markets_query
from .borrows import top_borrows_query
from .borrows import top_borrows_with_collateral_query

queries = {
    "top_markets": top_markets_query,
    "top_borrows": top_borrows_query,
    "top_borrows_with_collateral": top_borrows_with_collateral_query
}