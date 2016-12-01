import quandl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

start_date = '2015-06-10'
end_date = '2015-11-20'

amazon = quandl.get('YAHOO/AMZN', start_date=start_date, end_date=end_date).dropna()

plt.figure(figsize=(20,4))
plt.plot(amazon['Close'], label='Amazon')
xa = plt.axes().xaxis
xa.set_major_formatter(mdates.DateFormatter('%d'))
xa.set_major_locator(ticker.MultipleLocator(1))
xa.set_minor_locator(ticker.MultipleLocator(1))
