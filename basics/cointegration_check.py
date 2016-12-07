import quandl
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt

start_date = '2015-11-01'
end_date = '2016-11-01'


s1 = quandl.get('YAHOO/PEP', start_date=start_date, end_date=end_date).dropna()
s2 = quandl.get('YAHOO/KO', start_date=start_date, end_date=end_date).dropna()

plt.plot(s1['Close'], label='Facebook')
plt.plot(s2['Close'], label='Apple')
plt.legend()

(coint_t, p_value, crit_values) = ts.coint(s1['Close'], s2['Close'])

help(ts.coint)
