import quandl
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt

start_date = '2015-11-01'
end_date = '2016-11-01'


fb = quandl.get('YAHOO/FB', start_date=start_date, end_date=end_date).dropna()
apple = quandl.get('YAHOO/AAPL', start_date=start_date, end_date=end_date).dropna()

plt.plot(fb['Close'], label='Facebook')
plt.plot(apple['Close'], label='Apple')
plt.legend()

co = ts.coint(fb['Close'], apple['Close'])

print('Based on the pvalue there is a %f change the two time series are cointegrated' % co[1])
