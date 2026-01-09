import requests
import os
from .queries import queries, variables

SUBGRAPH_URL = "https://api.v3.aave.com/graphql"

class AaveApiClient:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
        }
    
    def query(self, query_name: str):
        response = requests.post(
            SUBGRAPH_URL,
            headers=self.headers,
            json={
                "query": queries[query_name],
                "variables": variables[query_name]
            }
        )
        return response.json()

    def get_top_markets(self, first: int = 10):
        res = self.query("markets")
        token_supply = {}
        # AaveV3Ethereum
        for market in res["data"]["markets"]:
            for reserve in market["reserves"]:
                token_supply[reserve["underlyingToken"]["symbol"]] = float(reserve["size"]["usd"])
        return sorted(token_supply.items(), key=lambda x: x[1], reverse=True)[:first]

if __name__ == "__main__":
    client = AaveApiClient()
    print(client.get_top_markets())