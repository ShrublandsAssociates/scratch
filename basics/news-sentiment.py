import quandl
import matplotlib.pyplot as plt

quandl.ApiConfig.api_key = 'rUwo7yshph3zGbitGEyw'

start_date = '2014-01-01'
end_date = '2014-05-01'

apple = quandl.get('YAHOO/AAPL', start_date=start_date, end_date=end_date).dropna()
apple_news_sentiment = quandl.get('AOS/AAPL', start_date=start_date, end_date=end_date).dropna()

plt.plot(apple['Close'].pct_change() * 100, label = 'Close')
plt.plot(apple_news_sentiment['Article Sentiment'] * apple_news_sentiment['Impact Score'] / 10, label = 'News')
plt.legend()
