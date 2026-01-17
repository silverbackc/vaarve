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

    def get_and_store_top_borrows(self, unique: bool = False):
        borrows = self.get_top_borrows()
        df = pd.DataFrame(borrows)
        df["asset"] = df["asset"].apply(lambda x: x["symbol"])
        df["account"] = df["account"].apply(lambda x: x["id"])
        if unique:
            df = df.drop_duplicates(subset=["id"])
            df.to_csv(f"{data_path}/top_borrows_unique.csv", index=False)
        else:
            df.to_csv(f"{data_path}/top_borrows.csv", index=False)
        return df

    def get_and_store_top_deposits(self):
        deposits = self.client.query("top_deposits", variables={"first": self.first})
        df = pd.DataFrame(deposits["data"]["deposits"])
        df["asset"] = df["asset"].apply(lambda x: x["symbol"])
        df["account"] = df["account"].apply(lambda x: x["id"])
        df.to_csv(f"{data_path}/top_deposits.csv", index=False)

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

    def get_and_store_top_two_accounts(self):
        accounts = self.client.query("top_two_accounts")
        df = pd.DataFrame(accounts["data"]["accounts"])
        df["deposits_amount_usd"] = df["positions"].apply(lambda x: sum([float(y["amountUSD"]) for p in x for y in p["deposits"]]))
        df["borrows_amount_usd"] = df["positions"].apply(lambda x: sum([float(y["amountUSD"]) for p in x for y in p["borrows"]]))
        df.drop(columns=["positions"], inplace=True)
        df.to_csv(f"{data_path}/top_two_accounts.csv", index=False)

    def get_and_store_deposits_for_accounts(self, account_ids: list[str]):
        accounts_nb = len(account_ids)
        step = 10
        df = pd.DataFrame(columns=["account", "amountUSD", "amount", "asset_symbol", "asset_decimals"])
        for i in range(0, accounts_nb, step):
            res = self.client.query("deposits", variables={"first": 3600, "account_ids": list(account_ids[i:i+step])})
            df_tmp = pd.DataFrame(res["data"]["deposits"])
            df_tmp["asset_symbol"] = df_tmp["asset"].apply(lambda x: x["symbol"])
            df_tmp["asset_decimals"] = df_tmp["asset"].apply(lambda x: x["decimals"])
            df_tmp["account"] = df_tmp["account"].apply(lambda x: x["id"])
            df_tmp.drop(columns=["asset"], inplace=True)
            df = pd.concat([df, df_tmp])
        df.to_csv(f"{data_path}/deposits_for_accounts.csv", index=False)
