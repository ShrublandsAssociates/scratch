import quandl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import pacf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
import statsmodels.formula.api as statsm
import statsmodels.tsa.vector_ar as var
import statsmodels.tsa.api as mod
import statsmodels.graphics.regressionplots as statsgraph
import prettytable as prettyT
import pyfolio as pf
import math 
import pylab as py
#import plotly.plotly as py
#import theano

# Quandl Key
quandl.ApiConfig.api_key = "rUwo7yshph3zGbitGEyw"

###Calling in the Top 3 Stocks US names from Quandl
Microsoft = quandl.get("WIKI/MSFT")
GE = quandl.get("WIKI/GE")
Amazon = quandl.get("WIKI/AMZN")

dateRangeStart = '2013-07-01'
dateRangeEnd = '2016-07-01'

###Calling in the 3YEAR Top 3 Stocks US names from Quandl
#Microsoft = Microsoft[dateRangeStart:dateRangeEnd].dropna()
#GE = GE[dateRangeStart:dateRangeEnd].dropna()
#Amazon = Amazon[dateRangeStart:dateRangeEnd].dropna()

###Calling in the Top 10 Stocks by market cap US names from Quandl
#Apple = quandl.get('WIKI/AAPL')
#Alphabet = quandl.get("WIKI/GOOG")
#Microsoft = quandl.get("WIKI/MSFT")
#Exxon = quandl.get("WIKI/XON")
#FaceBook = quandl.get("WIKI/FB")
#JohnsonJ = quandl.get("WIKI/JNJ")
#GE = quandl.get("WIKI/GE")
#Amazon = quandl.get("WIKI/AMZN")
#WellsFargo = quandl.get("WIKI/WFC")
#WallMart = quandl.get("WIKI/WMT")
##extras call ins seeking fro Co-integration
#Google = quandl.get("WIKI/GOOGL")
#GLD = quandl.get("LSE/GLD")
#GDX = quandl.get("LSE/GDX")
#JPM = quandl.get("WIKI/JPM")
#Citi = quandl.get("WIKI/C")
#Goldman = quandl.get("WIKI/GS")
#BOA = quandl.get("WIKI/BAC")
#Barclays = quandl.get("GOOG/LON_BARC")
#HSBC = quandl.get("GOOG/LON_HSBA")
#RBS = quandl.get("GOOG/LON_RBS")
#StanChart = quandl.get("GOOG/LON_STAN")
#Lloyds = quandl.get("GOOG/LON_LLOY")
# NB selections for co-integation against oil stocks
RDA = quandl.get("GOOG/LON_RDSA")
RDB = quandl.get("GOOG/LON_RDSB")

BP = quandl.get("LSE/BP")
Total = quandl.get("YAHOO/TTFNF")
ENI = quandl.get("GOOG/AMS_ENI")
Repsol = quandl.get("GOOG/PINK_REPYY")
Centrica = quandl.get("GOOG/LON_CNA")

# High R squared but still not co-integrated
#CreditSuisse = quandl.get("YAHOO/CSGKF")
#DB = quandl.get("GOOG/FRA_DBK")

###Calling in the 3YEAR Top 10 Stocks US names from Quandl
#Apple = Apple[dateRangeStart:dateRangeEnd].dropna()
#Alphabet = Alphabet[dateRangeStart:dateRangeEnd].dropna()
#Microsoft = Microsoft[dateRangeStart:dateRangeEnd].dropna()
#Exxon = Exxon[dateRangeStart:dateRangeEnd].dropna()
#FaceBook = FaceBook[dateRangeStart:dateRangeEnd].dropna()
#JohnsonJ = JohnsonJ[dateRangeStart:dateRangeEnd].dropna()
#GE = GE[dateRangeStart:dateRangeEnd].dropna()
#Amazon = Amazon[dateRangeStart:dateRangeEnd].dropna()
#WellsFargo = WellsFargo[dateRangeStart:dateRangeEnd].dropna()
#WallMart = WallMart[dateRangeStart:dateRangeEnd].dropna()
###extras
#Google = Google[dateRangeStart:dateRangeEnd].dropna()
#GLD = GLD[dateRangeStart:dateRangeEnd].dropna()
#GDX = GDX[dateRangeStart:dateRangeEnd].dropna()
#JPM = JPM[dateRangeStart:dateRangeEnd].dropna()
#Citi = Citi[dateRangeStart:dateRangeEnd].dropna()
#Goldman = Goldman[dateRangeStart:dateRangeEnd].dropna()
#BOA = BOA[dateRangeStart:dateRangeEnd].dropna()
#Barclays = Barclays[dateRangeStart:dateRangeEnd].dropna()
#HSBC = HSBC[dateRangeStart:dateRangeEnd].dropna()
#RBS = RBS[dateRangeStart:dateRangeEnd].dropna()
#Lloyds = Lloyds[dateRangeStart:dateRangeEnd].dropna()
#StanChart = StanChart[dateRangeStart:dateRangeEnd].dropna()

# 3 year data selected for co-integration
RDA =RDA[dateRangeStart:dateRangeEnd].dropna()
RDB = RDB[dateRangeStart:dateRangeEnd].dropna()
BP = BP[dateRangeStart:dateRangeEnd].dropna()
Total =Total[dateRangeStart:dateRangeEnd].dropna()
#ENI = ENI[dateRangeStart:dateRangeEnd].dropna()
Repsol = Repsol[dateRangeStart:dateRangeEnd].dropna()
Centrica = Centrica[dateRangeStart:dateRangeEnd].dropna()

#CreditSuisse =CreditSuisse[dateRangeStart:dateRangeEnd].dropna()
#DB = DB[dateRangeStart:dateRangeEnd].dropna()

# Testing for stationarity and using the Augmented Dicky Fuller Test
#lm(formula=z.diff-z.lag.1+tt+z.diff.lag)
#z.diff=delta_Yt & z.lag.1=Y(t-1) & 1=constant & tt=Time Trend=beta*time & z.diff.lag=delta_Y(t-1)
def stationary_test(stock, name = 'Test'):    
    rolling_mean50 = stock.rolling(window = 50, center = False).mean()
    rolling_mean200 = stock.rolling(window = 200, center = False).mean()
    rolling_std = stock.rolling(window = 50, center = False).std()
    plt.plot(stock.values,label='Stock Price',color='Black')
    plt.plot(rolling_mean50.values, label='50 Day',color='yellow')
    plt.plot(rolling_mean200.values, label='200 Day',color='green')
    plt.plot(rolling_std.values, label='Rolling Std',color='red')
    #plt.plot(rolling_mean50.values+rolling_std.values*2, label='Bollinger Upper',color='pink')
    #plt.plot(rolling_mean50.values-rolling_std.values*2, label='Bollinger Lower',color='pink')
    plt.title("50 & 200 Day MA's with Std ", fontsize=12)
    plt.legend( loc='best', fontsize=8 )
    plt.xlabel('3 Year Time Series in Days', fontsize=10)
    plt.ylabel('Stock Price, ' + str(name), fontsize=10)
    plt.savefig('test.jpg')
    plt.show()
    result = adfuller(stock)
    tstats = result[0]
    pvalue = result[1]
    table = prettyT.PrettyTable(['Stats', name])
    table.add_row(['t-value', tstats])
    table.add_row(['p-value', pvalue])
    table.add_row(['1%-critical', result[4]['1%']])
    table.add_row(['5%-critical', result[4]['5%']])
    table.add_row(['10%-critical', result[4]['10%']])
    print table
    if (tstats > result[4]['5%']):
        print("Time Series is likely Non Stationary")
        print(result)
    else:
        print("Time Series is likely Stationary")
        print(result)
    return result
  
# Plotting GE Share Prices From Financials Stoocks for 3 year time series
#print GE['Close']
#len(GE['Close'])
#mean=np.mean(GE['Close'])
#print(mean)
#plt.plot(GE['Close'])
#plt.hlines(mean,0,Barclays[dateRangeStart:]['Close'],linestyles='dashed',colors='red')
#plt.hlines(mean.values,0,len(Barclays['Close']),linestyles='dashed',colors='red')
#Barclays[dateRangeStart:]
#rolling_mean50 = stock.rolling(window = 50, center = False).mean()
#plt.plot(rolling_mean50.values, label='50 Day',color='yellow')
#plt.title('Times Series', fontsize=10)
#plt.xlabel('Time Series in Days')
#plt.ylabel('GE Share Price')
#plt.show()

RDA['Close'].plot()
RDB['Close'].plot()
#BP['Last Close'].plot()
Total['Close'].plot()
Repsol['Close'].plot()
Centrica['Close'].plot()
plt.yscale('Log')
plt.legend( loc='best', fontsize=8, labels = ["Royal Dutch A","Royal Dutch B","Total","Repsol","Centrica"] )
plt.xlabel('3 Year Time Series in Days', fontsize=10)
plt.ylabel('Log of Prices', fontsize=10)
plt.title('Times Series', fontsize=10)
#plt.hlines('log',0,len('log'),linestyles='dashed',colors='red')
plt.show()


#list=np.random.standard_normal(1000)
#list=py.hist(list,bins=100)
#plt.hist(list,normed=True)
#Hist=py.hist(Total['Close'],bins=100)
#histdate=py.hist(Hist,bins=12,alpha=.3)
#x=np(xlims[0],xlims[1],500)
#plt.legend( loc='best', fontsize=8, labels = ["Total"] )
#plt.xlabel('3 Year Time Series in Days', fontsize=10)
#plt.title('Total SA Times Series', fontsize=10)
#plt.show()

# Plotting Daily Returns for each Share Price From Financials Stoocks for 3 year time series
#def daily_return(prices, axis = 1 ).dropna()
#Testing for Stationarity on itself for each individual stock

def DailyReturn(Prices):
    returns = Prices.shift(1)/Prices -1
    return returns.dropna()
    
ReturnTotal = DailyReturn(Total['Close'])
ReturnCentrica = DailyReturn(Repsol['Close'])

stationary_test(ReturnTotal, name = 'Total Returns')

#######
#Spread Stationarity
######
#Testing for Stationarity on RDA, RDB, Total, Repsol and Centrica 
#Testing for Stationarity on RDA, RDB
concMergered = [RDA['Close'], RDB['Close']]
combo = pd.concat(concMergered, axis = 1 ).dropna()
combo.columns=["RDA","RDB"]
model = statsm.ols(formula = "RDA~RDB", data = combo)
result1 = model.fit()
result1.params
result1.summary()
#plt.plot(result,label='Ordinary least Squares',color='Black')
# graph of best fit
#statsgraph.plot_fit(result, 1,label='Ordinary least Squares',color='Black')
statsgraph.plot_fit(result1, 1)

#Testing for Stationarity on Ge, ?, R^2 should be near 1 ( best so far 68% ge on Amazon)
# Apple, exxon, Wells  no
# Microsoft, facebook, WallMart so so
#JohnsonJ not great
####### Amazon & Alphabet 68%
#Apple on Google 43%
# JPM-Wells 67%, Citi no,BOA no, Goldamn 50%
# Barcalys - Lloyds 43%-HSBC 62%-Stan 54%-RBS 55%

# royal Dutch is stationary hence strong evidence of cointgeration
# Credit Suisse - DB 86%
#concMergeredCO = [BP['Close'], RDA['Close']]
#Another example Centrica and repsol
concMergeredCO = [Centrica['Close'], Repsol['Close']]
comboCO = pd.concat(concMergeredCO, axis = 1 ).dropna()
comboCO.columns=["Centrica","Repsol"]
model = statsm.ols(formula = " Centrica~Repsol", data = comboCO)
resultCO = model.fit()
resultCO.params
resultCO.summary()
statsgraph.plot_fit(resultCO, 1)

b0=resultCO.params[0]
b1=resultCO.params[1]
spread=Centrica['Close']-(b0+b1*Repsol['Close'])
#spread=RDA['Open']-(b0+b1*RDB['Open'])
spread=spread.dropna()
stationary_test(spread, name = 'Spread')

# Demonstrates clarity for the error term in the model parameters against the residuals
# No drift term
residualsCO = resultCO.resid
#residualsCO.summary()
plt.title('Conintegration for Centrica and Repsol', fontsize=10)
stationary_test(residualsCO, name = 'Stationarity Test on the Spread')

#######Partial Auto correlation function PACF & ACF
acfTotal=acf(residualsCO)
plot_acf(acfTotal)
pacfTotal=pacf(residualsCO)
plot_pacf(pacfTotal)

# Please Note
#E[Yt=Bo/1-B1]
#expectation=result1.params[0]/(1-result1.params[1]-result1.params[2])
#print(expectation)
# Please Note
#V[Yt=sigma^2/1-B1^2]
#expectation=result1.params[0]/(1-result1.params[1]-result1.params[2])



# Multi-Variate
concMergeredMV =[RDA['Close'],RDB['Close'],Total['Close'],Repsol['Close'], Centrica['Close']]
comboMV = pd.concat(concMergeredMV, axis = 1 ).dropna()
comboMV.columns=["RDA", "RDB", "Total", "Repsol", "Centrica"]
model = statsm.ols(formula = "RDA~RDB+Total+Repsol+Centrica", data = comboMV)
resultMV = model.fit()
resultMV.params
resultMV.summary()
statsgraph.plot_fit(resultMV, 1)
#######Partial Auto correlation function PACF & ACF
residualsMV = resultMV.resid
acfModel=acf(residualsMV)
plot_acf(acfModel)
acfModel.summary()
pacfModel=pacf(residualsMV)
plot_pacf(pacfModel)
####################
# Lag 2
model=mod.VAR(comboMV)
model.select_order(10)

varlag=2
results=model.fit(varlag)
#results.summary()
coefs = results.coefs[varlag - 1]
residuals = results.resid

stationary_test(residuals, name = 'Stationarity Test on the Spread')
plt.plot(residuals)
plt.legend( loc='best', fontsize=8, labels = ["Royal Dutch A","Royal Dutch B","Total","Repsol","Centrica"] )
plt.xlabel('3 Year Time Series in Days', fontsize=10)
plt.title('Times Series', fontsize=10)
#plt.hlines('log',0,len('log'),linestyles='dashed',colors='red')
plt.show()
#Stability check
#all modulus less than 1
eigenvalues = np.absolute(np.linalg.eigvals(coefs))
print(eigenvalues)


comboMV.to_csv("C:/Users/Paidi/CQF/Project/OilData.csv")
residuals.to_csv("C:/Users/Paidi/CQF/Project/ResidualsOilData.csv")

### UKFinancial VAR(p) #####
#comboMV.to_csv("C:/Users/Paidi/CQF/Project/Oildata.csv")
#Optiminal lag is 2 by Akaike Information Criterion(AIC)
Stabdiff = comboMV.diff(periods = varlag, axis = 0).dropna()
listOfResults = []
listOfResultsResiduals = []
for col in comboMV.columns:
   # print combo[col]
    listOfResults.append(stationary_test(Stabdiff[col]))
    listOfResultsResiduals.append(stationary_test(residuals[col]))

######### Pyfolio #######
#Snapshot of facebook Characteristics

BP = pf.utils.get_symbol_rets('BP')
pf.create_returns_tear_sheet(BP, live_start_date = '2016-01-01')

##### Backtesting ####

bestFit = pd.read_csv("C:/Users/Paidi/CQF/Project/bestFitOilData.csv")
print(bestFit)
#bestFit.columns = ['~', 'bestFit']
#bestFit = bestFit['bestFit']
bestFit.columns = ['~', 'bestFit']
bestFit = bestFit['bestFit']



coef = pd.read_csv("C:/Users/Paidi/CQF/Project/coefOilData.csv")
coef.columns = ['~', 'Coeff']
Coeff = coef['Coeff']

residJo = pd.read_csv("C:/Users/Paidi/CQF/Project/ResidualsJoOilData.csv")

tau = 252
print(coef)
#speedReversion = -math.log(Coeff[0])/tau
#equilibriumMean = Coeff[1]/(1- Coeff[0])
speedReversion = -math.log(-Coeff[0])/tau
equilibriumMean = Coeff[1]/(1- Coeff[0])
SDcointResdiuals =math.sqrt(2*speedReversion*np.var(bestFit)/(1-math.exp(-2*speedReversion*tau)))
SDEq = SDcointResdiuals/math.sqrt(2*speedReversion)
halflife = math.log(2)/speedReversion

plt.plot(bestFit)
plt.hlines(np.average(bestFit) + SDEq, 0, 552,linestyles='dashed',colors='pink')
plt.hlines(np.average(bestFit), 0, 552,linestyles='dashed',colors='red')
plt.hlines(np.average(bestFit) - SDEq, 0, 552,linestyles='dashed',colors='pink')
plt.show()

sellThreshold = np.average(bestFit) + SDEq
buyThreshold = np.average(bestFit) - SDEq

#### Appendix #######################
#2
#backtesting loop
#each day, see if value of bestFit is higher than the sell Threshold or lower than the buy Threshold
countTrading = 0
position = "nothing"
for i in range(len(bestFit)):
    if (bestFit[i] > sellThreshold):
        print "close long"        
        print "short"
        position = "short"
        countTrading += 1
        
        #sell stock according to weights
    if (position == "short" and bestFit[i] < np.average(bestFit)):
        print "close short"
        position = "nothing"
        
    if (bestFit[i] < buyThreshold):
        #buy stock according to weights
        print "close short"
        print "long"
        position = "long"
        countTrading += 1
    if (position == "long" and bestFit[i] > np.average(bestFit)):
        print "close long"
        position = "nothing"
        
#### Appendix #######################
#3       
# Calling in Data from Yahoo for closing prices on 5 UK financial stocks and FTSE100 cash   
# Barclays data and 3 year data   
Barclays = pd.read_csv('C:/Users/Paidi/CQF/Project/Barclays.csv', index_col = 'Date').dropna()
Barclays['Close'].plot()
Barclays_3YR = pd.read_csv('C:/Users/Paidi/CQF/Project/Barclays_3YR.csv', index_col = 'Date').dropna()
# HSBC data and 3 year data
HSBC = pd.read_csv('C:/Users/Paidi/CQF/Project/HSBC.csv', index_col = 'Date').dropna()
HSBC['Close'].plot()
HSBC_3YR = pd.read_csv('C:/Users/Paidi/CQF/Project/HSBC_3YR.csv', index_col = 'Date').dropna()
# RBS data and 3 year data
RBS = pd.read_csv('C:/Users/Paidi/CQF/Project/RBS.csv', index_col = 'Date').dropna()
RBS['Close'].plot()
RBS_3YR = pd.read_csv('C:/Users/Paidi/CQF/Project/RBS_3YR.csv', index_col = 'Date').dropna()
# Lloyds data and 3 year data
Lloyds = pd.read_csv('C:/Users/Paidi/CQF/Project/Lloyds.csv', index_col = 'Date').dropna()
Lloyds['Close'].plot()
Lloyds_3YR = pd.read_csv('C:/Users/Paidi/CQF/Project/Lloyds_3YR.csv', index_col = 'Date').dropna()
# Standard Chatered data and 3 year data
StanChart = pd.read_csv('C:/Users/Paidi/CQF/Project/StanChart.csv', index_col = 'Date').dropna()
StanChart['Close'].plot()
StanChart_3YR = pd.read_csv('C:/Users/Paidi/CQF/Project/StanChart_3YR.csv', index_col = 'Date').dropna()
# Standard Chatered data and 3 year data
FTSE100 = pd.read_csv('C:/Users/Paidi/CQF/Project/FTSE100.csv', index_col = 'Date').dropna()
FTSE100['Close'].plot()
FTSE100_3YR = pd.read_csv('C:/Users/Paidi/CQF/Project/FTSE100_3YR.csv', index_col = 'Date').dropna()