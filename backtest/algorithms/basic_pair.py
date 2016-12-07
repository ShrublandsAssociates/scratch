# -*- coding: utf-8 -*-
from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import load_from_yahoo

def run(pair, start, end, z_threshold, window):
    class Pairtrade(TradingAlgorithm):

        def initialize(context):
            context.in_short = False
            context.in_long = False
            context.p1 = context.symbol(pair[0])
            context.p2 = context.symbol(pair[1])
            context.window = window
            context.i = 0

        def handle_data(context, data):
            context.i += 1
            if context.i < context.window:
                return
            s1_history = data.history(context.p1, 'price', context.window, '1d')
            s2_history = data.history(context.p2, 'price', context.window, '1d')
            diff = (s1_history - s2_history)
            mean = diff.mean()
            s1_price = data.current(context.p1, 'price')
            s2_price = data.current(context.p2, 'price')
            zscore = ((s1_price - s2_price) - diff.mean()) / diff.std()
            context.record(zscore = zscore, s1=s1_price, s2=s2_price)

            if zscore > z_threshold and not context.in_short:
                context.order_target_percent(context.p1, -0.5)
                context.order_target_percent(context.p2, 0.5)
                context.in_short = True
            elif zscore < -z_threshold and not context.in_long:
                context.order_target_percent(context.p1, 0.5)
                context.order_target_percent(context.p2, -0.5)
                context.in_long = True
            elif abs(zscore) < .5:
                context.order_target_percent(context.p1, 0)
                context.order_target_percent(context.p2, 0)
                context.in_short = False
                context.in_long = False

    data = load_from_yahoo(stocks=pair, indexes={}, start=start, end=end)
    pairtrade = Pairtrade()
    return pairtrade.run(data)
