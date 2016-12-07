# A z-score (aka, a standard score) indicates how many standard deviations an
# element is from the mean. A z-score can be calculated from the following
# formula.

# z = (X - μ) / σ

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# just set the seed for the random number generator
np.random.seed(106)

n = 50

# Generate the daily returns
X_returns = np.random.normal(0, 1, n)

# sum them and shift all the prices up into a reasonable range
X = pd.Series(np.cumsum(X_returns), name='X') + 50

some_noise = np.random.normal(0, 2, n)

Y = X + 5 + some_noise
Y.name = 'Y'

def zscore(series):
    return (series - series.mean()) / np.std(series)

def rolling_zscore(series, span=5):
    ewm = series.ewm(span=span)
    return (series - ewm.mean()) / ewm.std()

Xmean = X.ewm(span=5).mean()
Ymean = Y.ewm(span=5).mean()

# < -1 X long - Y short
# > 1 X short - Y long
# 0 close


f, (ax, ax1, ax2) = plt.subplots(3, sharex=True, figsize = (15, 10))
ax.set_title('Time Series', fontsize = 10)
ax.plot(X, color = 'red')
ax.plot(Y, color = 'blue')
ax1.plot(X - Xmean, label = 'X - Xμ', color = 'red')
ax1.plot(Y - Ymean, label = 'Y - Yμ', color = 'blue')
ax1.plot((X - Xmean) - (Y - Ymean), label = 'Diff')
ax2.set_title('Z score of X - Y', fontsize = 10)
ax2.plot(zscore(X-Y), color='black')
ax2.plot(rolling_zscore(X-Y), color='blue')
ax2.axhline(1.0, color='red', linestyle='--')
ax2.axhline(-1.0, color='green', linestyle='--')
