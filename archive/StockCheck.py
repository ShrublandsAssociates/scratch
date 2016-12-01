import quandl
import pandas as pd

# Quandl API Key - Without this quandl calls are rate limited
quandl.ApiConfig.api_key = "rUwo7yshph3zGbitGEyw"

START_DATE = '2013-10-01'
END_DATE = '2016-10-01'

def best_fit(df):
    return (df['ALB'] + df['ENS'] + df['FMC']) / 3

STOCK_DATA = {}
CLOSE_DATA = {}

STOCKS = {
    'ALB': 'YAHOO/ALB', #Albemarle
    'ENS': 'YAHOO/ENS', #EnerSys
    'FMC': 'YAHOO/FMC'
    }

for index in STOCKS:
    print('Fetching stock data for "', index, '"')
    if index in STOCK_DATA:
        print('Skip')
    else:
        STOCK_DATA[index] = quandl.get(STOCKS[index])[START_DATE:END_DATE].dropna()
        print('Fetching')
    CLOSE_DATA[index] = STOCK_DATA[index]['Close']


DF_CLOSE = pd.DataFrame(CLOSE_DATA)
shortMean = pd.rolling_mean(DF_CLOSE, 20)
longMean = pd.rolling_mean(DF_CLOSE, 100)

DF_CLOSE.plot()
best_fit(longMean).plot(linewidth = 2, color = 'red')
best_fit(shortMean).plot(linewidth = 2, color = 'black')