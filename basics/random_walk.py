import numpy as np
import pandas as pd

import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt

# just set the seed for the random number generator
np.random.seed(107)

# Generate the daily returns
X_returns = np.random.normal(0, 1, 100)

# sum them and shift all the prices up into a reasonable range
X = pd.Series(np.cumsum(X_returns), name='X') + 50

some_noise = np.random.normal(0, 1, 100)

Y = X + 5 + some_noise
Y.name = 'Y'
pd.concat([X, Y], axis=1).plot()
