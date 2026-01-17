import requests
import os
from .queries import queries
from dotenv import load_dotenv

load_dotenv()

# This Subgraph is provided by Messari
SUBGRAPH_URLS = {
    "aave": "",
    "messari": "https://gateway.thegraph.com/api/subgraphs/id/JCNWRypm7FYwV8fx5HhzZPSFaMxgkPuw4TnR3Gpi81zk"
}

class TheGraphClient:
    def __init__(self, subgraph: str = "messari"):
        self.subgraph = subgraph
        self.subgraph_url = SUBGRAPH_URLS[subgraph]
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('THE_GRAPH_API_KEY')}"
        }
    
    def query(self, query_name: str, variables: dict = None):
        response = requests.post(
            self.subgraph_url,
            headers=self.headers,
            json={
                "query": queries[query_name],
                "variables": variables
            }
        )
        return response.json()

    def get_top_assets(self, first: int = 10):
        res = self.query("top_markets", variables={"first": first})
        return [market["inputToken"]["symbol"] for market in res["data"]["markets"]]
