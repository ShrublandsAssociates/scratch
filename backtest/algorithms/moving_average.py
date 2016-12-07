# -*- coding: utf-8 -*-
from datetime import datetime
import pandas as pd
import pytz
import math
from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import load_from_yahoo

def run(symbol, startDate, endDate, startingCapital=100000):
    class MovingAverage(TradingAlgorithm):
        def initialize(self):
            self.stock = self.symbol(symbol)

        def handle_data(self, data):

            current_date=data.current_dt.strftime('%Y-%m-%d')
            if math.isnan(emaLong[current_date]):
                return

            if emaShort[current_date] > emaLong[current_date]:
                self.order_target(self.stock, 100)
            elif emaShort[current_date] < emaLong[current_date]:
                self.order_target(self.stock, 0)

            self.record(price=data.current(self.stock, 'price'), emaShort=emaShort[current_date])

    # Fetch Data
    data = load_from_yahoo(stocks=[symbol], indexes={}, start=startDate, end=endDate)

    stockReturns = data.tail(1)[symbol].values[0] - data.head(1)[symbol].values[0]

    # Setup
    emaShort = pd.rolling_mean(data[symbol], window = 100)
    emaLong = pd.rolling_mean(data[symbol], window = 200)

    # Back test
    simpleTrade = MovingAverage()
    results = simpleTrade.run(data)

    returnAmount = (results[-1:].portfolio_value.values[0] / startingCapital) - 1
    return (stockReturns, returnAmount, results)
