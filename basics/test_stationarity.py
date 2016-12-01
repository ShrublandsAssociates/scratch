import quandl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose

def test_stationarity(timeseries):

    #Determing rolling statistics
    rolling = timeseries.rolling(window=12)
    rolmean = rolling.mean()
    rolstd = rolling.std()
    plt.figure(figsize=(10,5))
    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)

    #Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)

fb_stock = quandl.get('YAHOO/FB', start_date=start_date, end_date=end_date).dropna()

# Is the stock stationary
test_stationarity(fb_stock['Close'])

# Can we use log to bring it down?
ts_log = np.log(fb_stock['Close'])
test_stationarity(ts_log)

# Is the different stationary
ts_log_diff = ts_log - ts_log.shift()
ts_log_diff.plot()
test_stationarity(ts_log_diff.dropna())

# Decompose
decomposition = seasonal_decompose(fb_stock['Close'], freq=1)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.plot(ts_log, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal,label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
