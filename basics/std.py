import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint

# just set the seed for the random number generator
np.random.seed(107)
returns = np.random.normal(0, 1, 10000)
ts = pd.Series(np.cumsum(X_returns), name='X') + 50
mean = returns - returns.mean()
x = returns - returns.mean()
plt.plot(ts)
plt.show()
plt.plot(x)
plt.show()
plt.hist(x, bins=50)

plt.scatter(ts)
