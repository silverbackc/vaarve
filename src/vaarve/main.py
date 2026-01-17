import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from scipy.stats import norm

from fetcher import top_markets_fetcher, price_fetcher, top_borrows_fetcher
from engine.bad_debt.bad_debt import BadDebtCalculator
from engine.vol.volatility import Volatility
from engine.simulation.simulator import Simulator
from engine.var.var import calculate_var


data_path = f"{os.path.dirname(os.path.abspath(__file__))}/data"
nb_simulations = int(os.getenv("SIMULATIONS", 10))


def plot_historical_and_simulated_prices(historical_prices: pd.DataFrame, simulated_prices: pd.DataFrame, asset: str, period: int = 30):
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)
    ax.plot(historical_prices.iloc[-period:][asset], label=f"{asset} last {period} days price")
    ax.plot(simulated_prices, linestyle='dashed')
    ax.set_title(f"{asset} last {period} days price and simulated prices")
    ax.set_xlabel("Days")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    ax.grid(True)
    fig.savefig(f"{data_path}/plots/{asset}_price_history_last_{period}_days_and_simulated.png")
    print(f"Saved {asset} price history last {period} days and simulated prices to {data_path}/plots/{asset}_price_history_last_{period}_days_and_simulated.png")
    plt.close()


def plot_bad_debt_histogram(bad_debt: pd.DataFrame, nb_bins: int):
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    horizons = bad_debt.index
    for i, horizon in enumerate(horizons):
        ax = axes[i]
        ax.hist(bad_debt.loc[horizon], bins=nb_bins)
        ax.set_title(f"Bad debt histogram at horizon {horizon}D")
        ax.set_xlabel("Bad debt (USD)")
        ax.set_ylabel("Frequency")
        ax.grid(True)
    fig.tight_layout()
    fig.savefig(f"{data_path}/plots/bad_debt_histogram.png")
    print(f"Saved bad debt histogram to {data_path}/plots/bad_debt_histogram.png")
    plt.close()


def plot_centered_log_returns(log_returns: pd.Series, asset: str):
    centered_log_returns = (log_returns - log_returns.mean()) / log_returns.std()
    x = np.linspace(norm.ppf(0.001), norm.ppf(0.999), 1000)
    y = norm.pdf(x)
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)
    ax.hist(centered_log_returns, bins=50, density=True)
    ax.plot(x, y, label="Normal distribution")
    ax.legend()
    ax.set_title(f"{asset} centered log returns histogram and normal distribution")
    ax.set_xlabel("Centered log returns")
    ax.set_ylabel("Density")
    ax.grid(True)
    fig.savefig(f"{data_path}/plots/{asset}_centered_log_returns_histogram_and_normal_distribution.png")
    print(f"Saved {asset} centered log returns histogram and normal distribution to {data_path}/plots/{asset}_centered_log_returns_histogram_and_normal_distribution.png")
    plt.close()


if __name__ == "__main__":
    load_dotenv()
    # Latest tokens from top10 markets by supply
    top_tokens = ['WETH', 'weETH', 'USDT', 'wstETH', 'USDC', 'WBTC', 'cbBTC', 'USDe', 'sUSDe', 'RLUSD']
    refresh = os.getenv("REFRESH", "False").lower() == "true"
    if refresh:
        print("Refreshing data...")
        price_fetcher.get_and_store_price_history(top_tokens)
        print("Price history stored")

        top_borrows_fetcher.get_and_store_top_borrows()
        print("Top borrows stored")

        top_borrows_fetcher.get_and_store_top_borrows_with_collateral()
        print("Top borrows with deposits stored")

        top_tokens = top_markets_fetcher.get_top_markets()
        print(f"Top tokens by supply: {top_tokens}")

    top_borrows = pd.read_csv(f"{data_path}/top_borrows.csv")
    print(f"Total borrowed amount (USD): {top_borrows['amountUSD'].sum()}")
    print("Top assets borrowed amount (USD):")
    print(top_borrows.groupby("asset")["amountUSD"].sum().sort_values(ascending=False))

    # Load price history and compute volatility
    period = 90
    price_history = pd.read_csv(f"{data_path}/price_history.csv")
    volatility = Volatility(price_history)
    volatility.calculate_vol_log_returns(period)
    print(f"Total volatility of log returns for the last {period} days:")
    print(volatility.log_returns_std)
    plot_centered_log_returns(volatility.log_returns["WETH"], asset="WETH")

    # Simulate prices for top tokens
    horizons = [1, 7, 14]
    simulator = Simulator(volatility, horizons)
    simulated_prices = simulator.simulate_price(nb_simulations)

    weth_sim_prices = simulated_prices["WETH"]
    tmp_df = pd.DataFrame([[price_history.iloc[-1]["WETH"]] * nb_simulations], index=[365], columns=range(nb_simulations))
    weth_sim_prices_init = pd.concat([tmp_df, weth_sim_prices])
    plot_historical_and_simulated_prices(price_history, weth_sim_prices_init, "WETH")

    # Calculate bad debt for top tokens and top borrows
    top_borrows_with_collateral = pd.read_csv(f"{data_path}/top_borrows_with_collateral.csv")
    bad_debt_calculator = BadDebtCalculator(top_borrows_with_collateral, simulated_prices, top_tokens)
    current_bad_debt = bad_debt_calculator.calculate_current_bad_debt()
    print(f"Total number of accounts: {len(current_bad_debt)}")
    print(f"Total bad debt: {current_bad_debt.sum()}")
    filtered_current_bad_debt = current_bad_debt[current_bad_debt > 0]
    print(f"Number of accounts with bad debt: {len(filtered_current_bad_debt)}")
    
    bad_debt_per_trajectory = bad_debt_calculator.calculate_portfolio_bad_debt()
    bad_debt_per_trajectory.index = horizons
    plot_bad_debt_histogram(bad_debt_per_trajectory, int(nb_simulations/5))

    confidence_levels = [0.9, 0.95, 0.99]
    vars_df = calculate_var(bad_debt_per_trajectory, confidence_levels, horizons)
    print(vars_df)
