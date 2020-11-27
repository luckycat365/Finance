import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import numpy as np
import statsmodels.api as sm

df=pd.read_csv('PFE.csv', parse_dates=True, index_col=0)  #parse_dates and index_col=0 are used to use dates as index
short_window = 10
long_window = 30
signals = pd.DataFrame(index=df.index) #create a new dataframe, use df's index as index
signals['Signal'] = 0
signals['Short_Average'] = df['Close'].rolling(window=short_window,min_periods=1).mean()
signals['Long_Average'] = df['Close'].rolling(window=long_window,min_periods=1).mean()

signals['Signal'][short_window:] = np.where(signals['Short_Average'][short_window:] > signals['Long_Average'][short_window:],1,0 )
signals['positions'] = signals['Signal'].diff()
print(signals)
#print('New',df['Close'])
fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Price in $')
df['Close'].plot(ax=ax1, color='r', lw=2.)
signals[['Short_Average','Long_Average']].plot(ax=ax1, lw=2.)


# Plot the buy signals
ax1.plot(signals.loc[signals.positions == 1.0].index, 
         signals.Short_Average[signals.positions == 1.0],
         '^', markersize=10, color='m')

# Plot the sell signals
ax1.plot(signals.loc[signals.positions == -1.0].index, 
         signals.Short_Average[signals.positions == -1.0],
         'v', markersize=10, color='k')
#ax.plot(signals.index, signals['Short_Average'])
#ax.plot(signals.index, signals['Long_Average'])
plt.show()