import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

def bestfit(x, y):
    return (x + y) / 2

# Generate some data
x=np.arange(100)
y1=np.sin(x / 6)
y2=y1 + np.random.uniform(size=100)
y3=y2 + np.random.uniform(size=100)
yr=np.random.uniform(size=100)

bf = bestfit(y2, y3)

plt.plot(y2, color = 'red')
plt.plot(y3, color = 'green')
plt.plot(pd.rolling_mean(bf, 15), color = 'blue')
plt.show()
plt.scatter(y2, y3)



# Pearson Correlation. Is this a good
corrcoef = np.corrcoef(y2, y3)[0, 1]
if abs(corrcoef) > 0.8:
    print('This is a good correlation', corrcoef)
else:
    print('This is a bad correlation', corrcoef)
