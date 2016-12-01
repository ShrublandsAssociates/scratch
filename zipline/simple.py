# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from algorithms.moving_average import run

(stockReturn, algorithmReturn, results) = run(symbol = 'FB', startDate = '2012-01-01', endDate = '2013-01-01')
results.emaShort

# Show results
f, (sp1, sp2, sp3) = plt.subplots(3, figsize=(18,9))
sp1.plot(results.price)
sp1.plot(emaShort, label = 'emaShort')
sp1.plot(emaLong, label = 'emaLong')
sp1.legend()
sp2.plot(results.portfolio_value)
sp3.plot(emaLong - emaShort, label = 'MACD')
sp3.plot((emaSignal - emaLong) / emaLong, label = 'Signal')
plt.show()

returnAmount = (results[-1:].portfolio_value.values[0] / startingCapital) - 1
print(returnAmount)
