import quandl
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt

import statsmodels.formula.api as statsm
from statsmodels.tsa.stattools import adfuller

quandl.ApiConfig.api_key = 'rUwo7yshph3zGbitGEyw'

start_date = '2015-07-01'
end_date = '2016-07-01'

stock_list = [ 'GOOG/NYSE_PXD', 'GOOG/NYSE_CVX', 'GOOG/NYSEARCA_IAU', 'GOOG/NYSE_DGZ', 'GOOG/LON_SGBS' ]
#stock_list = [ 'GOOG/NYSE_PXD', 'GOOG/NYSE_CVX', 'GOOG/NYSEARCA_IAU']
def fetch_stock_data(stocks, start_date, end_date):
    return_stocks = {}
    for stock in stocks:
        return_stocks[stock] = quandl.get(stock, start_date=start_date, end_date=end_date).dropna()['Close']
    return return_stocks

stock_data = fetch_stock_data(stock_list, start_date, end_date)

def print_coint(ts_a, ts_b):
    concMergered = [ts_a,ts_a]
    combo = pd.concat(concMergered, axis = 1 ).dropna()
    combo.columns=["a","b"]
    model = statsm.ols(formula = "a~b", data = combo)

    ols_results = model.fit()

    if ols_results.rsquared > 0.5:
        print('There is a %f chance of cointegration' % ols_results.rsquared)
    print(ols_results.summary())

    # Can we get high confidence that the pair are co-int. Use Johanson?

    stationary_results = adfuller(ols_results.resid)
    #if abs(stationary_results[0]) > abs(stationary_results[4]['5%']):
    #    print('Residuals are stationary ')

i = 1
for stock_a in stock_list:
    for stock_b in stock_list[i:]:
        print(stock_a, stock_b)
        print_coint(stock_data[stock_a], stock_data[stock_b])
    i += 1
