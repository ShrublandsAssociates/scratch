# -*- coding: utf-8 -*-
import quandl
import pandas as pd
import matplotlib.pyplot as plt

from portfolio import Portfolio
from run_test import run_test

quandl.ApiConfig.api_key = 'rUwo7yshph3zGbitGEyw'

START_DATE = '2015-01-01'
END_DATE = '2016-11-06'

stock = quandl.get('YAHOO/FB', start_date=START_DATE,end_date=END_DATE).dropna()

ema_short = pd.ewma(stock['Close'], 5)
ema_long = pd.ewma(stock['Close'], 20)

portfolio = Portfolio(10000)

def rebalance(context, stock_data, index):
    print(111, context['is_high'])
    stock_price = stock_data['Close']
    if context.is_high == False and ema_short[index] > ema_long[index]:
        context.is_high = True
        context.is_low = False
        context.portfolio.close_orders(stock_price, lambda o: o.symbol == 'FB')
    if context.is_low == False and ema_short[index] < ema_long[index]:
        context.is_low = True
        context.is_high = False
        context.portfolio.place_order(context.balance / stock_price, stock_price, 'FB')

run_test({ 'portfolio': portfolio, 'is_high': False, 'is_low': False }, stock, rebalance)

portfolio.close_orders(stock[-1:]['Close'])

print('End balance', portfolio.balance)

plt.plot(stock['Close'], label = 'Close')
plt.plot(stock['Equity'], label = 'Equity')
plt.plot(ema_short, label = '5')
plt.plot(ema_long, label = '20')
plt.legend(loc = 'upper left')
