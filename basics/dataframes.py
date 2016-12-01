import pandas as pd
import numpy as np
dt = '2016-01-01'
rng = pd.date_range('2016-01-01', '2016-03-01')
ts = pd.Series(np.random.randn(len(rng)), index=rng)
ts = pd.Timestamp(dt)
ts.strftime('%Y-%m-%d')
type(ts)
