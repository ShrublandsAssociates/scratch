# -*- coding: utf-8 -*-

import numpy as np
from datetime import datetime
import pandas as pd
import pytz
import math
from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import load_from_yahoo

class PairsTradingAlgorithm(TradingAlgorithm):
    def initialize(context):
        context.stock1 = context.symbol('PXD')
        context.stock2 = context.symbol('CVX')

        # Our threshold for trading on the z-score
        context.entry_threshold = 0.2
        context.exit_threshold = 0.1

        # Moving average lengths
        context.long_ma_length = 30
        context.short_ma_length = 1

        # Flags to tell us if we're currently in a trade
        context.currently_long_the_spread = False
        context.currently_short_the_spread = False


    def handle_data(context, data):

        # For notational convenience
        s1 = context.stock1
        s2 = context.stock2

        # Get pricing history
        #prices = context.history([s1, s2], "price", context.long_ma_length, '1d')
        prices = context.history(s1, field = 'Close', frequency = '1d')
        print(prices)
        # Try debugging me here to see what the price
        # data structure looks like
        # To debug, click on the line number to the left of the
        # next command. Line numbers on blank lines or comments
        # won't work.
        short_prices = prices.iloc[-context.short_ma_length:]

        # Get the long mavg
        long_ma = np.mean(prices[s1] - prices[s2])
        # Get the std of the long window
        long_std = np.std(prices[s1] - prices[s2])


        # Get the short mavg
        short_ma = np.mean(short_prices[s1] - short_prices[s2])

        # Compute z-score
        if long_std > 0:
            zscore = (short_ma - long_ma)/long_std

            # Our two entry cases
            if zscore > context.entry_threshold and \
                not context.currently_short_the_spread:
                context.order_target_percent(s1, -0.5) # short top
                context.order_target_percent(s2, 0.5) # long bottom
                context.currently_short_the_spread = True
                context.currently_long_the_spread = False

            elif zscore < -context.entry_threshold and \
                not context.currently_long_the_spread:
                context.order_target_percent(s1, 0.5) # long top
                context.order_target_percent(s2, -0.5) # short bottom
                context.currently_short_the_spread = False
                context.currently_long_the_spread = True

            # Our exit case
            elif abs(zscore) < context.exit_threshold:
                context.order_target_percent(s1, 0)
                context.order_target_percent(s2, 0)
                context.currently_short_the_spread = False
                context.currently_long_the_spread = False
u
            context.record('zscore', zscore)


# Fetch Data
data = load_from_yahoo(stocks=['PXD', 'CVX'], indexes={}, start = datetime(2012, 3, 1, 0, 0, 0, 0, pytz.utc), end = datetime(2014, 3, 1, 0, 0, 0, 0, pytz.utc))

# Back test
simpleTrade = PairsTradingAlgorithm(start = datetime(2013, 5, 1, 0, 0, 0, 0, pytz.utc), end = datetime(2014, 3, 1, 0, 0, 0, 0, pytz.utc))
results = simpleTrade.run(data)
