# A beta of 1 indicates that the security's price moves with the market. A beta
# of less than 1 means that the security is theoretically less volatile than the
# market. A beta of greater than 1 indicates that the security's price is
# theoretically more volatile than the market. For example, if a stock's beta is
# 1.2, it's theoretically 20% more volatile than the market. Conversely, if an
# ETF's beta is 0.65, it is theoretically 35% less volatile than the market.
# Therefore, the fund's excess return is expected to underperform the benchmark
# by 35% in up markets and outperform by 35% during down markets.

import quandl
import numpy as np
import statsmodels.api as sm

quandl.ApiConfig.api_key = 'rUwo7yshph3zGbitGEyw'

start_date = '2015-11-01'
end_date = '2016-11-01'

tech_index = quandl.get('YAHOO/INDEX_NYA-NYSE-Composite-Index', start_date=start_date, end_date=end_date).dropna()
fb_stock = quandl.get('YAHOO/FB', start_date=start_date, end_date=end_date).dropna()
tesla_stock = quandl.get('YAHOO/TSLA', start_date=start_date, end_date=end_date).dropna()

def beta(a, b):
    covariance = np.cov(a, b)
    return covariance[0, 1] / covariance[1, 1]

beta(tech_index['Close'], fb_stock['Close'])
