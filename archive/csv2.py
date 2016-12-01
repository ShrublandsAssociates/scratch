# -*- coding: utf-8 -*-
import pandas as pd
import quandl
START_DATE = '2016-05-01'
END_DATE = '2016-11-06'

quandl.ApiConfig.api_key = "rUwo7yshph3zGbitGEyw"
stock = quandl.get('YAHOO/FB')[START_DATE:END_DATE].dropna()

data = pd.read_csv('~/Development/javascript/stocks/facebook.csv', index_col = 0, parse_dates = True)
data = data.sort_index()

#data['change'] = (stock['Open'] - stock['Close']) * 4
data.plot()
(data['count'] * data['sentiment']).plot()

# Show Volitility
(stock['Close'] /stock['Open'] - 1).hist();

stock['Close'].plot()
shortMean = pd.ewma(stock['Close'], 5).plot()
longMean = pd.ewma(stock['Close'], 20).plot()
longMean = pd.ewma(stock['Close'], 40).plot()
