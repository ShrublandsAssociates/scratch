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

import quandl
import numpy as np

quandl.ApiConfig.api_key = 'rUwo7yshph3zGbitGEyw'

start_date = '2015-11-01'
end_date = '2016-11-01'

spy = quandl.get('YAHOO/INDEX_SPY', start_date=start_date, end_date=end_date).dropna()
fb_stock = quandl.get('YAHOO/FB', start_date=start_date, end_date=end_date).dropna()
tesla_stock = quandl.get('YAHOO/TSLA', start_date=start_date, end_date=end_date).dropna()

def annualised_sharpe(returns, N = 252):
    """
    Calculate the annualised Sharpe ratio of a returns stream
    based on a number of trading periods, N. N defaults to 252,
    which then assumes a stream of daily returns.

    The function assumes that the returns are the excess of
    those compared to a benchmark.
    """
    return np.sqrt(N) * returns.mean() / returns.std()

def market_neutral_sharpe(stock, benchmark):
    """
    Calculates the annualised Sharpe ratio of a market
    neutral long/short strategy inolving the long of 'stock'
    with a corresponding short of the 'benchmark'.
    """
    return annualised_sharpe((stock - benchmark) / 2)

# Facebook is 10 times riskier than S&P500
annualised_sharpe(spy['Close'].pct_change())
annualised_sharpe(fb_stock['Close'].pct_change())
annualised_sharpe(tesla_stock['Close'].pct_change())
market_neutral_sharpe(fb_stock['Close'].pct_change(), spy['Close'].pct_change())
market_neutral_sharpe(tesla_stock['Close'].pct_change(), spy['Close'].pct_change())
