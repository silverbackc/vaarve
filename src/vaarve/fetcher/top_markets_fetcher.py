import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clients.the_graph.client import TheGraphClient

class TopMarketsFetcher:
    def __init__(self, first: int = 10):
        self.client = TheGraphClient()
        self.first = first

    def get_top_markets(self):
        return self.client.get_top_assets(self.first)


if __name__ == "__main__":
    fetcher = TopMarketsFetcher()
    print(fetcher.get_top_markets())