import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt

# just set the seed for the random number generator
np.random.seed(107)

# Generate the daily returns
X_returns = np.random.normal(0, 1, 100)

# sum them and shift all the prices up into a reasonable range
X = pd.Series(np.cumsum(X_returns), name='X') + 5

some_noise = np.random.normal(0, .5, 100)

Y = X + 5 + some_noise
Y.name = 'Y'
pd.concat([X, Y], axis=1).plot()

def are_correlated(ts_a, ts_b):
    concMergered = [ts_a, ts_b]
    combo = pd.concat(concMergered, axis = 1).dropna()
    combo.columns=["a","b"]
    model = statsm.ols(formula = "a~b", data = combo)
    ols_results = model.fit()

    # Can we get higher confidence that the pair are co-int. Use Johanson?
    results = adfuller(ols_results.resid, regression='ct')

    is_strong = abs(results[0]) > abs(results[4]['1%'])

    return (is_strong, results[0], results[1])

are_correlated(X, Y)
