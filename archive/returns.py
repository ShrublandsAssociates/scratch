# -*- coding: utf-8 -*-

import quandl
import pandas as pd
import matplotlib.pyplot as plt

START_DATE = '2015-01-01'
END_DATE = '2016-11-06'

quandl.ApiConfig.api_key = "rUwo7yshph3zGbitGEyw"
stock = quandl.get('YAHOO/FB')(start_date = START_DATE, end_date = END_DATE).dropna()
stock['Equity'] = 0
ema_short = pd.ewma(stock["Close"], 5)
ema_long = pd.ewma(stock["Close"], 20)

plt.plot(stock["Close"], label = 'Close')
plt.plot(ema_short, label = '5')
plt.plot(ema_long, label = '20')
plt.legend(loc = 'upper left')


def calculate_return(invesetment, balance):
    print('P&L', balance - investment)
    print('%', balance  / investment)

def close_position(number_shares):
    global balance, sell_price, shares
    if number_shares > 0:
        balance = sell_price * number_shares
        shares -= number_shares
        print('Sell ', number_shares, ' at ', buy_price)

def get_profit_loss (current_price):
    global shares
    return (current_price - buy_price) * shares

def get_equity (current_price):
    return balance + get_profit_loss(current_price)

is_low = False
is_high = False
investment = 1000
balance = investment
shares = 0
buy_price = 0
sell_price = 0
profit_loss = 0

for i in stock.index:
    stock_price = stock['Close'][i]
    if (is_high == False and ema_short[i] > ema_long[i]):
        is_high = True
        is_low = False
        sell_price = stock_price
        close_position(shares)
    if (is_low == False and ema_short[i] < ema_long[i]):
        is_low = True
        is_high = False
        buy_price = stock_price
        shares  =  balance / buy_price
        balance = 0
        print('Buy ', shares, ' at ', buy_price)

#    stock['Equity'][i] = get_equity(stock_price)
    print(is_low, is_high, balance, shares)

close_position(shares)
print(balance, shares)
calculate_return(investment, balance)

plt.plot(stock["Close"], label = 'Close')
plt.plot(stock["Equity"], label = 'Equity')
plt.plot(ema_short, label = '5')
plt.plot(ema_long, label = '20')
plt.legend(loc = 'upper left')
