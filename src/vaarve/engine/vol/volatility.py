import pandas as pd
import numpy as np
from typing import Optional


class Volatility:
    def __init__(self, price_history: pd.DataFrame):
        self.price_history = price_history
        self.log_returns = None
        self.log_returns_mean = None
        self.log_returns_std = None
        self.log_returns_cov = None
        self.log_returns_var = None

    def calculate_vol_log_returns(self, period: Optional[int] = None):
        log_returns = self.price_history.apply(lambda x: np.log(x / x.shift(1)))
        self.log_returns = log_returns
        if period:
            log_returns = log_returns.iloc[-period:]
        self.log_returns_mean = log_returns.mean()
        self.log_returns_std = log_returns.std()
        self.log_returns_cov = log_returns.cov()
        self.log_returns_var = log_returns.var()
