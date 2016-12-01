# -*- coding: utf-8 -*-

import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.sandbox.regression.predstd import wls_prediction_std

# Generate some data
x = np.arange(100)
ys = np.sin(x / 6) + x / 12
y1 = ys + np.random.uniform(size = 100) * 2
y2 = 3 + ys + np.random.uniform(size = 100)
yr = np.random.uniform(size = 100)


results = sm.OLS(y1, y2).fit()

plt.plot(y1)
plt.plot(y2)
plt.plot(pd.rolling_mean(results.fittedvalues, 5), color = 'black')
plt.plot(pd.rolling_mean(results.fittedvalues, 15), color = 'red')
plt.show()
plt.scatter(y1, y2)
plt.show()

# Inspect the results
print(results.summary())

results.resid
pstd, l, u = wls_prediction_std(results)
plt.plot(pstd)
bf = (u + l) / 2
plt.plot(l - bf)
plt.plot(u - bf)

plt.plot(l)
plt.plot(u)
