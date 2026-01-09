import os

from .top_markets_fetcher import TopMarketsFetcher
from .price_fetcher import PriceFetcher
from .top_borrows import TopBorrowsFetcher

max_borrows = 1000
max_markets = int(os.getenv("MAX_MARKETS", 5))

top_markets_fetcher = TopMarketsFetcher(max_markets)
price_fetcher = PriceFetcher()
top_borrows_fetcher = TopBorrowsFetcher(max_borrows)
