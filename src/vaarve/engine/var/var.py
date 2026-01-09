import pandas as pd

def calculate_var(bad_debt: pd.DataFrame, confidence_levels: list[float], horizons: list[int]):
    vars_df = pd.DataFrame(index=horizons, columns=confidence_levels)
    for confidence_level in confidence_levels:
        for horizon in horizons:
            var = bad_debt.loc[horizon].quantile(confidence_level)
            vars_df.loc[horizon, confidence_level] = var
    return vars_df