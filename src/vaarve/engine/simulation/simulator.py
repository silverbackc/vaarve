import numpy as np
import pandas as pd
from engine.vol.volatility import Volatility

class Simulator:
    def __init__(self, volatility: Volatility, horizons: list[int]) -> None:
        self.volatility = volatility
        self.nb_assets = len(volatility.price_history.columns)
        self.horizons = horizons

    def simulate_price(self, iterations: int):
        multi_index = pd.MultiIndex.from_product([self.volatility.price_history.columns, range(iterations)])
        simulated_prices = pd.DataFrame(index=[365 + h for h in self.horizons], columns=multi_index)
        time_horizons = np.array(self.horizons)
        for i in range(self.nb_assets):
            random_numbers = np.random.randn(len(self.horizons), iterations)
            drift = (self.volatility.log_returns_mean.iloc[i] - 0.5 * self.volatility.log_returns_var.iloc[i]) * time_horizons
            log_returns = drift[:, np.newaxis] + self.volatility.log_returns_std.iloc[i] * random_numbers * np.sqrt(time_horizons[:, np.newaxis])
            starting_point = self.volatility.price_history.iloc[-1][i]
            sim_prices = starting_point * np.exp(log_returns)
            simulated_prices[self.volatility.price_history.columns[i]] = sim_prices
        return simulated_prices
