# The Sharpe Ratio is a measure for calculating risk-adjusted return, and this
# ratio has become the industry standard for such calculations. It was developed
# by Nobel laureate William F. Sharpe. The Sharpe ratio is the average return
# earned in excess of the risk-free rate per unit of volatility or total risk.
# Subtracting the risk-free rate from the mean return, the performance
# associated with risk-taking activities can be isolated. One intuition of this
# calculation is that a portfolio engaging in “zero risk” investment, such as
# the purchase of U.S. Treasury bills (for which the expected return is the
# risk-free rate), has a Sharpe ratio of exactly zero. Generally, the greater
# the value of the Sharpe ratio, the more attractive the risk-adjusted return.

import numpy as np

def annualised(returns, N = 252):
    """
    Calculate the annualised Sharpe ratio of a returns stream
    based on a number of trading periods, N. N defaults to 252,
    which then assumes a stream of daily returns.

    The function assumes that the returns are the excess of
    those compared to a benchmark.
    """
    diff = returns.pct_change()
    return np.sqrt(N) * diff.mean() / diff.std()

def market_neutral(stock, benchmark):
    """
    Calculates the annualised Sharpe ratio of a market
    neutral long/short strategy inolving the long of 'stock'
    with a corresponding short of the 'benchmark'.
    """
    return annualised((stock - benchmark) / 2)
