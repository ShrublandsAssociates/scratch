""""
Example
"""

import quandl
import pandas as pd
import statsmodels.tsa.api as mod

import matplotlib.pyplot as plt
# import statsmodels.graphics.regressionplots as statsgraph


# Quandl API Key - Without this quandl calls are rate limited
quandl.ApiConfig.api_key = "rUwo7yshph3zGbitGEyw"

START_DATE = '2013-07-01'
END_DATE = '2016-07-01'


STOCKS = {
    'GDX': 'GOOG/NYSEARCA_GDX', 
    'GLD': 'GOOG/NYSEARCA_GLD', 
    'IAU': 'GOOG/NYSEARCA_IAU', 
    'DGZ': 'GOOG/NYSE_DGZ'
    }

STOCK_DATA = {}
CLOSE_DATA = []
COLUMNS = []

# Fetch the stock data for all the required stocks
for index in STOCKS:
    print('Fetching stock data for "', index, '"')
    STOCK_DATA[index] = quandl.get(STOCKS[index])[START_DATE:END_DATE].dropna()
    CLOSE_DATA.append(STOCK_DATA[index]['Close'])
    COLUMNS.append(index)

# Plot closing prices
for index in STOCKS:
    STOCK_DATA[index]['Close'].plot()

plt.yscale('Log')
plt.legend( loc = 'best', fontsize = 8, labels = COLUMNS )
plt.xlabel('3 Year Time Series in Days', fontsize = 10)
plt.ylabel('Log of Prices', fontsize = 10)
plt.title('Times Series', fontsize = 10)
plt.show()


comboMV = pd.concat(CLOSE_DATA, axis = 1).dropna()
comboMV.columns = COLUMNS
#model = statsm.ols(formula = "RDA~RDB+Total+Repsol+Centrica", data = comboMV)

model = mod.VAR(comboMV)
model.select_order(10)

varlag = 2
results = model.fit(varlag)
cvsData = results.resid.stack().reset_index()
cvsData.to_csv('GoldResiduals.csv', header = ['Date', 'Symbol', 'Value'], index =  False)