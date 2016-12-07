import quandl
from stock import sharpe
quandl.ApiConfig.api_key = 'rUwo7yshph3zGbitGEyw'

start_date = '2015-11-01'
end_date = '2016-11-01'

spy = quandl.get('YAHOO/INDEX_SPY', start_date=start_date, end_date=end_date).dropna()
fb_stock = quandl.get('YAHOO/FB', start_date=start_date, end_date=end_date).dropna()
tesla_stock = quandl.get('YAHOO/TSLA', start_date=start_date, end_date=end_date).dropna()

# Facebook is 10 times riskier than S&P500
sharpe.annualised(spy['Close'])
sharpe.annualised(fb_stock['Close'])
sharpe.annualised(tesla_stock['Close'])
sharpe.market_neutral(fb_stock['Close'], spy['Close'])
sharpe.market_neutral(tesla_stock['Close'], spy['Close'])
