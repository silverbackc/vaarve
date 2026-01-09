import pandas as pd
import time
from typing import Optional
import os

from clients import CoingeckoClient

data_path = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/data"

cg_mapping = {
    "WETH": "ethereum",
    "weETH": "wrapped-eeth",
    "USDT": "tether",
    "wstETH": "wrapped-steth",
    "USDC": "usd-coin",
    "WBTC": "wrapped-bitcoin",
    "cbBTC": "coinbase-wrapped-btc",
    "USDe": "ethena-usde",
    "sUSDe": "ethena-staked-usde",
    "RLUSD": "ripple-usd",
}

class PriceFetcher:
    def __init__(self, symbols: Optional[list[str]] = None):
        self.symbols = symbols
        self.client = CoingeckoClient()

    def get_and_store_price_history(self, symbols: Optional[list[str]] = None):
        if symbols:
            self.symbols = symbols
        df = pd.DataFrame()
        for symbol in self.symbols:
            res = self.client.get_price_history(cg_mapping[symbol])
            time.sleep(1)
            df[symbol] = [row[1] for row in res]
        df.to_csv(f"{data_path}/price_history.csv", index=False)
