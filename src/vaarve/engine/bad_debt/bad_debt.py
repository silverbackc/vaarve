import pandas as pd
import ast

def compute_dollar_value(amount: float, price: float, asset_decimals: int):
    return amount * price / 10 ** asset_decimals

def health_factor(borrow_usd: float, deposit_usd: float, liquidation_threshold: float):
    return deposit_usd * liquidation_threshold / borrow_usd

class BadDebtCalculator:
    def __init__(self, portfolio: pd.DataFrame, simulated_prices: pd.DataFrame, top_assets: pd.DataFrame):
        self.supported_assets = top_assets["symbol"].tolist()
        self.average_liquidation_thresholds = top_assets["liquidation_threshold"].astype(float).mean() / 100
        self.portfolio = portfolio.copy()
        self.portfolio["deposits"] = self.portfolio["deposits"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        self.portfolio = self.portfolio[self.portfolio["asset_symbol"].isin(self.supported_assets)]
        self.simulated_prices = simulated_prices
        self.bad_debt_per_trajectory = pd.DataFrame(0.0, index=simulated_prices.index, columns=simulated_prices.columns.levels[1])
        
    def compute_deposits_dollar_value(self, deposits, prices: pd.Series, trajectory: int):
        amount_usd = 0
        for deposit in deposits:
            amount = float(deposit["amount"])
            asset_decimals = int(deposit["asset"]["decimals"])
            asset_symbol = deposit["asset"]["symbol"]
            if asset_symbol not in self.supported_assets:
                continue
            price = prices[(asset_symbol, trajectory)]
            amount_usd += compute_dollar_value(amount, price, asset_decimals)
        return amount_usd

    def calculate_bad_debt_per_trajectory_per_step(self, trajectory: int, step: int, accounts_to_exclude: list[str]):
        portfolio_bd = self.portfolio.copy()
        portfolio_bd = portfolio_bd[~portfolio_bd["account_id"].isin(accounts_to_exclude)]
        portfolio_bd["borrow_usd"] = portfolio_bd.apply(lambda x: compute_dollar_value(float(x["amount"]), self.simulated_prices.loc[step, (x["asset_symbol"], trajectory)], int(x["asset_decimals"])), axis=1)
        portfolio_bd["deposit_usd"] = portfolio_bd["deposits"].apply(lambda x: self.compute_deposits_dollar_value(x, self.simulated_prices.loc[step, :], trajectory))
        portfolio_borrows_by_user = portfolio_bd.groupby("account_id")["borrow_usd"].sum()
        portfolio_deposits_by_user = portfolio_bd.groupby("account_id")["deposit_usd"].first()
        portfolio_bad_debt_by_user = portfolio_borrows_by_user - portfolio_deposits_by_user
        return portfolio_bad_debt_by_user.apply(lambda x: max(0, x))

    def calculate_current_bad_debt(self):
        portfolio_bd = self.portfolio.copy()
        portfolio_bd["deposit_usd"] = portfolio_bd["deposits"].apply(lambda x: sum([float(v["amountUSD"]) for v in x]))
        portfolio_bd["deposits_count"] = portfolio_bd["deposits"].apply(lambda x: len(x))
        portfolio_borrows_by_user = portfolio_bd.groupby("account_id", as_index=False)["amountUSD"].sum()
        portfolio_deposits_by_user = portfolio_bd.groupby("account_id", as_index=False)[["deposits_count", "deposit_usd"]].first()
        pf_joint = pd.merge(portfolio_borrows_by_user, portfolio_deposits_by_user, on="account_id", how="left")
        pf_joint["health_factor"] = pf_joint.apply(lambda x: health_factor(x["amountUSD"], x["deposit_usd"], self.average_liquidation_thresholds), axis=1)
        pf_joint["bad_debt"] = pf_joint.apply(lambda x: max(0, x["amountUSD"] - x["deposit_usd"]), axis=1)
        return pf_joint

    def calculate_portfolio_bad_debt(self, accounts_to_exclude: list[str]):
        for trajectory in self.simulated_prices.columns.levels[1]:
            for t in self.simulated_prices.index:
                bad_debt_per_user = self.calculate_bad_debt_per_trajectory_per_step(trajectory, t, accounts_to_exclude)
                self.bad_debt_per_trajectory.loc[t, trajectory] = bad_debt_per_user.sum()
        return self.bad_debt_per_trajectory