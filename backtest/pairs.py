import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
from datetime import datetime
import pytz

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import load_from_yahoo

start = datetime(2016, 1, 1, 0, 0, 0, 0, pytz.utc)
end = datetime(2016, 12, 1, 0, 0, 0, 0, pytz.utc)

pair = ['AMZN', 'FB'] # 6%
pair = ['RRC', 'HAL'] # 119%
data = load_from_yahoo(stocks=pair, indexes={}, start=start, end=end)

z_threshold = 1

class Pairtrade(TradingAlgorithm):

    def initialize(context):
        context.in_short = False
        context.in_long = False
        context.p1 = context.symbol(pair[0])
        context.p2 = context.symbol(pair[1])
        context.window = 20
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

pairtrade = Pairtrade()
results = pairtrade.run(data)
f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize = (15, 10))
ax1.plot(results.portfolio_value)
ax2.plot(results.s1, label = pair[0])
ax2.plot(results.s2, label = pair[1])
ax3.plot(results.zscore)
ax3.axhline(z_threshold, color='red', linestyle='--')
ax3.axhline(-z_threshold, color='green', linestyle='--')
profit = results.portfolio_value[-1]-results.portfolio_value[0]
return_pc = (results.portfolio_value[-1] / results.portfolio_value[0]) * 100
print(profit, return_pc)
