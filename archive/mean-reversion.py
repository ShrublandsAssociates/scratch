import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.tsa.arima_model as am
import math


def bestfit(x, y):
    return (x + y) / 2

sample_size = 500
# Generate some data
x = np.arange(sample_size)
y1 = np.sin(x / 20)
y2 = y1 + np.random.uniform(size = sample_size)
y3 = y2 + np.random.uniform(size = sample_size)
yr = np.random.uniform(size = sample_size)


bf = bestfit(y2, y3)

coef = am.ARIMA(bf, [1,0,0]).fit().params

tau = 252

speedReversion = abs(coef[0]) / tau
equilibriumMean = coef[1]/(1 - coef[0])
SDcointResdiual = math.sqrt(2 * speedReversion * bf.var() / (1 - math.exp(-2*speedReversion*tau)))
SDEq = SDcointResdiual / math.sqrt(2*speedReversion)

# We are looking for a shortish halflife. > 50 days is too much
halflife = math.log(2) / speedReversion


short_mean = pd.rolling_mean(bf, 5)
long_mean = pd.rolling_mean(bf, 20)

weight = (long_mean - short_mean) / long_mean
normalize_weight = weight / weight[20:].sum()

plt.plot(bf, color = 'orange')
plt.plot(short_mean, color = 'red')
plt.plot(long_mean, color = 'green')
#plt.plot(weight , color = 'blue')
plt.plot(normalize_weight, color = 'black')


plt.show()
