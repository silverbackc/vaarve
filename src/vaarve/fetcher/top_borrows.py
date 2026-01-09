import pandas as pd
import os

from clients.the_graph.client import TheGraphClient

data_path = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/data"

class TopBorrowsFetcher:
    def __init__(self, first: int = 10):
        self.client = TheGraphClient()
        self.first = first

    def get_top_borrows(self):
        res = self.client.query("top_borrows", variables={"first": self.first})
        return res["data"]["borrows"]

    def get_and_store_top_borrows(self):
        borrows = self.get_top_borrows()
        df = pd.DataFrame(borrows)
        df["asset"] = df["asset"].apply(lambda x: x["symbol"])
        df.to_csv(f"{data_path}/top_borrows.csv", index=False)

    def get_top_borrows_with_collateral(self):
        res = self.client.query("top_borrows_with_collateral", variables={"first": self.first})
        return res["data"]["borrows"]

    def get_and_store_top_borrows_with_collateral(self):
        borrows = self.get_top_borrows_with_collateral()
        df = pd.DataFrame(borrows)
        df["asset_symbol"] = df["asset"].apply(lambda x: x["symbol"])
        df["asset_decimals"] = df["asset"].apply(lambda x: x["decimals"])
        df["account_id"] = df["account"].apply(lambda x: x["id"])
        df["deposits"] = df["account"].apply(lambda x: x["deposits"])
        df.drop(columns=["account", "asset"], inplace=True)
        df.to_csv(f"{data_path}/top_borrows_with_collateral.csv", index=False)


if __name__ == "__main__":
    fetcher = TopBorrowsFetcher()
    fetcher.get_and_store_top_borrows_with_collateral()