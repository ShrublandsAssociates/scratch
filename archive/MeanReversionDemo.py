# -*- coding: utf-8 -*-

import datetime
import quandl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import statsmodels.tsa.stattools as ts
from pandas.stats.api import ols
from johansen import johansen

def plot_scatter_series(df, ts1, ts2):
    plt.xlabel('%s Price ($)' % ts1)
    plt.ylabel('%s Price ($)' % ts2)
    plt.title('%s and %s Price Scatterplot' % (ts1, ts2))
    plt.scatter(df[ts1], df[ts2])
    plt.show()
    
def plot_residuals(df):
    months = mdates.MonthLocator()  # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df["res"], label="Residuals")
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(datetime.datetime(2012, 1, 1), datetime.datetime(2013, 1, 1))
    ax.grid(True)
    fig.autofmt_xdate()

    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('Residual Plot')
    plt.legend()

    plt.plot(df["res"])
    plt.show()
    

# Quandl API Key - Without this quandl calls are rate limited
quandl.ApiConfig.api_key = "rUwo7yshph3zGbitGEyw"

START_DATE = '2013-07-01'
END_DATE = '2016-07-01'


STOCKS = {
    'GDX': 'GOOG/NYSEARCA_GDX', 
    'GLD': 'GOOG/NYSEARCA_GLD'
    }

STOCK_DATA = {}
CLOSE_DATA = []
COLUMNS = []

# Fetch the stock data for all the required stocks
for index in STOCKS:
    print('Fetching stock data for "', index, '"')
    STOCK_DATA[index] = quandl.get(STOCKS[index])[START_DATE:END_DATE].dropna()
    CLOSE_DATA.append(STOCK_DATA[index]['Close'])
    COLUMNS.append(index)
    
comboMV = pd.concat(CLOSE_DATA, axis = 1).dropna()
comboMV.columns = COLUMNS

comboMV.plot()
plt.scatter(comboMV.GDX, comboMV.GLD)
res = ols(y = comboMV.GDX, x = comboMV.GLD)
res.resid.plot()

johansen(comboMV)