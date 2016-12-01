""""
Example
"""

import quandl
import pandas as pd
from statsmodels.tsa.stattools import coint 
import numpy as np
import matplotlib.pyplot as plt
# import statsmodels.graphics.regressionplots as statsgraph


# Quandl API Key - Without this quandl calls are rate limited
quandl.ApiConfig.api_key = "rUwo7yshph3zGbitGEyw"

START_DATE = '2013-07-01'
END_DATE = '2016-07-01'


STOCKS = {
    'PAAS': 'YAHOO/PAAS',
    'SLW': 'YAHOO/SLW',
    'CDE': 'YAHOO/CDE',
    'SSRI': 'YAHOO/SSRI'
    }

STOCK_DATA = {}
CLOSE_DATA = {}
COLUMNS = []

def zscore(series):  
    return (series - series.mean()) / np.std(series)

def visualize_spread(x, y):  
    score, pvalue, _= coint(x, y)  
    diff_series= x-y  
    zscore(diff_series).plot()  
    plt.axhline(zscore(diff_series).mean(), color='black')  
    plt.axhline(1.0, color='red', linestyle='--')  
    plt.axhline(-1.0, color='green', linestyle='--')  
    plt.figure(figsize=(15,8))  
    plt.show()

# Fetch the stock data for all the required stocks
for index in STOCKS:
    print('Fetching stock data for "', index, '"')
    if index in STOCK_DATA:
        print('Skip')
    else:
        STOCK_DATA[index] = quandl.get(STOCKS[index])[START_DATE:END_DATE].dropna()
        print('Fetching')
        CLOSE_DATA[index](STOCK_DATA[index]['Close'])


pd.
# Plot closing prices
for index in STOCKS:
    STOCK_DATA[index]['Close'].plot()

# For reference
SLW = STOCK_DATA['SLW']['Close']
PAAS = STOCK_DATA['PAAS']['Close']
PAAS.plot()
SLW.plot()
pd.rolling_var(SLW, 30).plot()
SLW.std()