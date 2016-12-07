# -*- coding: utf-8 -*-
import warnings
import matplotlib.pyplot as plt
import pytz
import pandas as pd
from datetime import datetime
from backtest.algorithms.basic_pair import run

warnings.filterwarnings('ignore')

z_threshold = 1
pair = ['ADBE', 'NFLX']

start = datetime(2015, 7, 1, 0, 0, 0, 0, pytz.utc)
end = datetime(2016, 7, 1, 0, 0, 0, 0, pytz.utc)

results = run(pair, start, end, z_threshold, 22)
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

pairs = pd.read_csv('../data/coint_tech_stock.csv', header=None)
output = pd.DataFrame(columns=['S1', 'S2', 'Corr', 'Profit', 'Returns'])
for row in pairs.iterrows():
    index, data = row
    pair = data[0:2].tolist()
    results = run(pair, start, end, z_threshold, 22)
    profit = results.portfolio_value[-1]-results.portfolio_value[0]
    return_pc = (results.portfolio_value[-1] / results.portfolio_value[0])
    output.loc[len(output)] = pair + [data[2]] + [profit, return_pc]
    print(','.join(pair),profit, return_pc)
