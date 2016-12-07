
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import math
# Create cointegrated correlated pair
np.random.seed(107)
n=200
returns = np.random.normal(0, 1, n)
noise = np.random.normal(1, 1, n)
X = pd.Series(np.cumsum(returns), name='X') + 50
Y = X + 5 + noise
Y.name = 'Y'
import quandl
start_date = '2015-11-01'
end_date = '2016-11-01'
X = quandl.get('YAHOO/GOOG', start_date=start_date, end_date=end_date)['Close'].dropna()
Y = quandl.get('YAHOO/TSO', start_date=start_date, end_date=end_date)['Close'].dropna()

pd.concat([X, Y], axis=1).plot();
plt.show()

def zscore(series):
    return (series - series.mean()) / np.std(series)

def plot_z(z, upper, lower):
    z.plot()
    plt.axhline(z.mean(), color='black')
    plt.axhline(upper, color='red', linestyle='--')
    plt.axhline(lower, color='green', linestyle='--')
    plt.legend(['Spread z-score', 'Mean', '+1', '-1'])

def hedge_ratio(Y, X) :
    return sm.OLS(Y, sm.add_constant(X)).fit().params[1]

def order_profit(order_price, current_price):
    if order_price == 0:
        return 0
    if order_price >= 0:
        return current_price - order_price
    else:
        return -order_price + abs(current_price)

def calc_share_count(capital, a_price, b_price):
    a_count = math.floor(capital * 0.5 / a_price)
    b_count = math.floor(capital * 0.5 / b_price)
    return a_count, b_count

def calculate_returns(series_a, series_b, capital = 10000, window=30):
    upper = 1
    lower = -1
    n = pd.DataFrame(columns=('capital', 'profit', 'a_order', 'b_order', 'a_price', 'b_price', 'z'))
    a_count = 0
    b_count = 0
    a_order = 0
    b_order = 0
    profit = 0
    has_position = False
    for i in range(window, len(series_a) - 1):
        series_a_window = series_a[i-window:i]
        series_b_window = series_b[i-window:i]
        slope, intercept = sm.OLS(series_b_window, sm.add_constant(series_a_window)).fit().params
        spread = series_b_window - slope * series_a_window + intercept
        z = zscore(spread)[i-window]
        profit = a_count * order_profit(a_order, series_a[i]) + b_count * order_profit(b_order, series_b[i])
        if not has_position and z < lower:
            a_count, b_count = calc_share_count(capital, series_a[i], series_b[i])
            a_order = series_a[i]
            b_order = -series_b[i]
            capital -= round(a_count * series_a[i] - b_count * series_b[i])
            has_position = True
        elif not has_position and z > upper:
            a_count, b_count = calc_share_count(capital, series_a[i], series_b[i])
            a_order = -series_a[i]
            b_order = series_b[i]
            capital -= round(a_count * series_a[i] - b_count * series_b[i])
            has_position = True
        elif has_position and abs(z) < 0.5:
            capital += profit
            has_position = False
            a_count = b_count = a_order = b_order = 0
        n.loc[i] = [ capital, profit, a_order, b_order, series_a[i], series_b[i], z ]

    profit = a_count * order_profit(a_order, series_a[i]) + b_count * order_profit(b_order, series_b[i])
    capital += profit
    #n.loc[i+1] = [ capital, profit, a_order, b_order, series_a[i], series_b[i], z[i] ]
    return n

calculate_returns(X, Y)
