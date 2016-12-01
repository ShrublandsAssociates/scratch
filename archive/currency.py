import quandl
import matplotlib.pyplot as plt


START_DATE = '2015-11-01'
END_DATE = '2016-11-01'

quandl.ApiConfig.api_key = "rUwo7yshph3zGbitGEyw"
euro_gbp = quandl.get('BOE/XUDLSER')[START_DATE:END_DATE].dropna()
gbp_eur = (1 / euro_gbp)

plt.plot(gbp_eur, color = 'orange', label = 'GBP->EUR')
plt.plot(pd.ewma(gbp_eur, 365), color = 'blue', label = 'EMA(365)')
plt.plot(pd.rolling_mean(gbp_eur, 150), color = 'red', label = 'Moving Average(365)')
plt.legend()
