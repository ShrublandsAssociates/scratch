# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sample_size = 100

# Generate some data
x = np.arange(sample_size)
x_sin = np.sin(x / 8)
x_ran = np.random.uniform(size=sample_size)
x_sin_with_noise = x_sin + x_ran

f, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.plot(pd.rolling_mean(x_sin, window=5), label='Sin')
ax1.plot(x_sin, '--', label='Sin Mean')
ax2.plot(x_sin_with_noise, label='Sin With Noise')
ax2.plot(pd.ewma(x_sin_with_noise, span=5), label='Sine With Noise Mean')
ax1.set_title('Simple Plot', fontsize = 10)
