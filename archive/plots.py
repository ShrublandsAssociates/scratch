import numpy as np
import matplotlib.pyplot as plt

# generate some data
x = np.arange(100)
y1 = np.sin(x / 6)
y2 = y1 + np.random.uniform(size = 100)
y3 = y2 + np.random.uniform(size = 100)
yr = np.random.uniform(size = 100)

y2unbiased = y2-np.mean(y2)
y1unbiased = y1-np.mean(y1)
y1norm = np.sum(y1unbiased**2)
acor = np.correlate(y1unbiased, y2unbiased, "same")/y1norm
# use only second half
#acor = acor[len(acor)/2:]

plt.plot(acor)
plt.plot(y2)
plt.plot(y3)
plt.show()
plt.scatter(y2, y3)


# Pearson Correlation. Is this a good 

corrcoef = np.corrcoef(y2, y3)[0, 1]
if abs(corrcoef) > 0.8:
    print('This is a good correlation', corrcoef)
else: 
    print('This is a bad correlation', corrcoef)