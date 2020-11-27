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
signals['Close']=df['Close']
print(signals)
#print('New',df['Close'])


###### Back Testing #################################

initial_capital = float(60000.0)
positions = pd.DataFrame(index=df.index).fillna(0)
positions['PFE'] = 100*signals['Signal']  # Buy a 100 shares

portfolio = positions.multiply(df['Close'], axis=0) #initialize the portfolio with value owned. df.multiply is pandas function to multiply 2 DFs axis=0 means to compare by index, axis =1 means compare by columns

#dftest = pd.DataFrame({'angles': [0, 3, 4],'N': [360, 180, 360]},index=['circle', 'triangle', 'rectangle'])
#print('ori \n',dftest)
#dftest2 = pd.Series([1,2,3],index=['circle','triangle', 'rectangle'])
#print('matrix \n',dftest2)
#result = dftest.multiply(dftest2,axis=0)
#print('restult \n',result)

print('Portfolio \n',portfolio)
pos_diff = positions.diff().fillna(0)   # store the difference in shares owned
print('difference \n', pos_diff)
#portfolio['holdings'] = (positions.multiply(df['Close'],axis=0)).sum(axis=1)
portfolio['holdings'] = (positions.multiply(df['Close'],axis=0)).sum(axis=1) #The sum() is applied on "positions" dataframe, not portfolio. add the columns of "positions" and store them in "portfolio"


portfolio['cash']=initial_capital - (pos_diff.multiply(df['Close'],axis=0)).sum(axis=1).cumsum(axis='index')
portfolio['total']=portfolio['cash']+portfolio['holdings']
portfolio['returns']=portfolio['total'].pct_change()
print('Portfolio new \n',portfolio)

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')
portfolio['total'].plot(ax=ax1, lw=2.)
ax1.plot(portfolio.loc[signals.positions == 1.0].index, portfolio.total[signals.positions==1.0],'^',markersize=10, color='g')
ax1.plot(portfolio.loc[signals.positions == -1.0].index, portfolio.total[signals.positions==-1.0],'v',markersize=10, color='r')
plt.show()

###### Calculate sharp ratio ##### the greater the ratio, the better. 1 is acceptable, 2 is very good, 3 is excellent
returns=portfolio['returns']
sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())
print(sharpe_ratio)

##### Maximum Drawdown ##### measure the largest single drop from peak to bottom. This indicates the risk of a portfolio
window = 252
rolling_max = df['Close'].rolling(window,min_periods=1).max()
daily_drawdown = df['Close']/rolling_max - 1.0
max_daily_drawdown = daily_drawdown.rolling(window,min_periods=1).min()

daily_drawdown.plot()
max_daily_drawdown.plot()
plt.show()


##### Compound Annual Growth Rate #####
days = (df.index[-1]-df.index[0]).days
cagr = ((((df['Adj Close'][-1]) / df['Adj Close'][1])) ** (365.0/days)) - 1
print('CARR',cagr)