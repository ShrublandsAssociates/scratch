import quandl
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as statsm
import statsmodels.tsa.api as mod
import statsmodels.graphics.regressionplots as statsgraph

#import plotly.plotly as py
#import theano

# Quandl Key
quandl.ApiConfig.api_key = "rUwo7yshph3zGbitGEyw"

###Calling in the Top 3 Stocks US names from Quandl

dateRangeStart = '2013-07-01'
dateRangeEnd = '2016-07-01'

RDA = quandl.get("GOOG/LON_RDSA")
RDB = quandl.get("GOOG/LON_RDSB")

BP = quandl.get("LSE/BP")
Total = quandl.get("YAHOO/TTFNF")
ENI = quandl.get("GOOG/AMS_ENI")
Repsol = quandl.get("GOOG/PINK_REPYY")
Centrica = quandl.get("GOOG/LON_CNA")

RDA =RDA[dateRangeStart:dateRangeEnd].dropna()
RDB = RDB[dateRangeStart:dateRangeEnd].dropna()
BP = BP[dateRangeStart:dateRangeEnd].dropna()
Total =Total[dateRangeStart:dateRangeEnd].dropna()
Repsol = Repsol[dateRangeStart:dateRangeEnd].dropna()
Centrica = Centrica[dateRangeStart:dateRangeEnd].dropna()

RDA['Close'].plot()
RDB['Close'].plot()
Total['Close'].plot()
Repsol['Close'].plot()
Centrica['Close'].plot()
plt.yscale('Log')
plt.legend( loc='best', fontsize=8, labels = ["Royal Dutch A","Royal Dutch B","Total","Repsol","Centrica"] )
plt.xlabel('3 Year Time Series in Days', fontsize=10)
plt.ylabel('Log of Prices', fontsize=10)
plt.title('Times Series', fontsize=10)
plt.show()

def DailyReturn(Prices):
    returns = Prices.shift(1)/Prices -1
    return returns.dropna()
    
ReturnTotal = DailyReturn(Total['Close'])
ReturnCentrica = DailyReturn(Repsol['Close'])

concMergered = [RDA['Close'], RDB['Close']]
combo = pd.concat(concMergered, axis = 1 ).dropna()
combo.columns=["RDA","RDB"]
model = statsm.ols(formula = "RDA~RDB", data = combo)
result1 = model.fit()
statsgraph.plot_fit(result1, 1)

concMergeredCO = [Centrica['Close'], Repsol['Close']]
comboCO = pd.concat(concMergeredCO, axis = 1 ).dropna()
comboCO.columns=["Centrica","Repsol"]
model = statsm.ols(formula = " Centrica~Repsol", data = comboCO)
resultCO = model.fit()

# Demonstrates clarity for the error term in the model parameters against the residuals
# No drift term
residualsCO = resultCO.resid

concMergeredMV =[RDA['Close'],RDB['Close'],Total['Close'],Repsol['Close'], Centrica['Close']]
comboMV = pd.concat(concMergeredMV, axis = 1 ).dropna()
comboMV.columns=["RDA", "RDB", "Total", "Repsol", "Centrica"]
model = statsm.ols(formula = "RDA~RDB+Total+Repsol+Centrica", data = comboMV)
resultMV = model.fit()
####################
# Lag 2
model=mod.VAR(comboMV)
#model.select_order(10)

varlag=2
results=model.fit(varlag)

coefs = results.coefs[varlag - 1]
residuals = results.resid

comboMV.to_csv("C:/Users/Paidi/CQF/Project/OilData.csv")
residuals.to_csv("C:/Users/Paidi/CQF/Project/ResidualsOilData.csv")
print('Complete')