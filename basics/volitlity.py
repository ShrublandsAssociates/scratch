import math
import numpy as np
import pandas as pd

# just set the seed for the random number generator
np.random.seed(107)

# Generate the daily returns
returns = np.random.normal(0, 0.1, 100)

# sum them and shift all the prices up into a reasonable range
X = pd.Series(np.cumsum(returns) * 6, name='X')
X.plot()

def compute_volatility(price_history):
    # Compute daily volatility
    historical_vol_daily = price_history.pct_change().dropna().std()

    # Convert daily volatility to annual volatility, assuming 252 trading days
    historical_vol_annually = historical_vol_daily * math.sqrt(252)

    # Return estimate of annual volatility
    return 100 * historical_vol_annually

compute_volatility(X)
