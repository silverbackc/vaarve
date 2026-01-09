import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.coingecko.com/api/v3"
API_KEY = os.getenv("COINGECKO_API_KEY")

class CoingeckoClient:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
        }
    
    def get_price_history(self, symbol: str):
        response = requests.get(
            f"{BASE_URL}/coins/{symbol}/market_chart?vs_currency=usd&days=365&interval=daily&x_cg_demo_api_key={API_KEY}"
        )
        return response.json()["prices"]

if __name__ == "__main__":
    client = CoingeckoClient()
    print(client.get_price_history("ethereum"))