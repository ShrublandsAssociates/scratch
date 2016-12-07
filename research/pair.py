import quandl
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt

import statsmodels.formula.api as statsm
from statsmodels.tsa.stattools import adfuller


def are_correlated(ts_a, ts_b):
    concMergered = [ts_a, ts_b]
    combo = pd.concat(concMergered, axis = 1).dropna()
    combo.columns=["a","b"]
    model = statsm.ols(formula = "a~b", data = combo)
    ols_results = model.fit()

    # Can we get higher confidence that the pair are co-int. Use Johanson?
    stationary_results = adfuller(ols_results.resid, regression='ct')
    help(adfuller)
    is_strong = abs(stationary_results[0]) > abs(stationary_results[4]['5%'])

    return (is_strong, ols_results.rsquared, stationary_results[0])
