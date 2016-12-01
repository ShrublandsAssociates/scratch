# -*- coding: utf-8 -*-
import pandas as pd
df = pd.read_csv('https://dl.dropboxusercontent.com/u/454411527/ResidualsOilDataConc.csv')
df.pivot(index = 'Date', columns = 'symbol', values = 'residuals')
