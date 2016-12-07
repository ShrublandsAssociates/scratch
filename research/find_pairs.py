import quandl
import pandas as pd
import statsmodels.formula.api as statsm
from statsmodels.tsa.stattools import adfuller

import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt

import os
cwd = os.getcwd()
quandl.ApiConfig.api_key = 'rUwo7yshph3zGbitGEyw'

start_date = '2015-07-01'
end_date = '2016-07-01'
symbols = pd.read_csv('../data/spy_full.tsv', sep="\t")

tech_symbols = symbols[symbols['Sector'] == 'Energy']['Symbol']

def fetch_stock_data(stocks, start_date, end_date):
    return_stocks = {}
    for stock in stocks:
        try:
            return_stocks[stock] = quandl.get('YAHOO/%s' % stock, start_date=start_date, end_date=end_date).dropna()['Close']
        except:
            pass
            print('Unable to load %s' % stock)
    return return_stocks

stock_data = fetch_stock_data(tech_symbols, start_date, end_date)

def are_correlated(ts_a, ts_b):
    concMergered = [ts_a, ts_b]
    combo = pd.concat(concMergered, axis = 1).dropna()
    combo.columns=["a","b"]
    model = statsm.ols(formula = "a~b", data = combo)
    ols_results = model.fit()

    # Can we get higher confidence that the pair are co-int. Use Johanson?
    results = adfuller(ols_results.resid, regression='ct')

    is_strong = abs(results[0]) > abs(results[4]['10%'])

    return (is_strong, results[0], results[1])


def find_pairs(stock_data):
    stock_list = list(stock_data.keys())
    i = 1
    pairs = []
    for stock_a in stock_list:
        for stock_b in stock_list[i:]:
            (is_strong, t_stat, p_value) = are_correlated(stock_data[stock_a], stock_data[stock_b])
            if is_strong:
                pairs.append((stock_a, stock_b, p_value))
        i += 1
    return pairs

possible_pairs = find_pairs(stock_data)
for p in possible_pairs:
    print(','.join(map(str, p)))

def plot_pair(stock_data, a, b):
    x = stock_data[a]
    y = stock_data[b]
    x.name = a
    y.name = b
    pd.concat([x - x.mean(), y - y.mean()], axis=1).plot()

plot_pair(stock_data, 'RRC', 'HAL')
#plot_pair(stock_data, 'AMZN', 'FB')
