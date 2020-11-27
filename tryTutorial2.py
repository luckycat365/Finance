import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import FinanceUtil as tool
import numpy as np

#try11='haha'
#print('try character is {}'.format(try11))

style.use('ggplot')
name='Multiple'
start = dt.datetime(2010, 1, 11)
end = dt.datetime.now()
#end = dt.datetime(2018, 1, 1)
#df = web.DataReader(name, 'yahoo', start, end)

tickers = ['NVDA','AMD', 'PFE','GOOG']
df=tool.gettickers(tickers,start,end)
#print(df)
daily_close_px = df['Close'].reset_index().pivot('Date', 'Ticker', 'Close')   # rearrange the table using Date as index, Ticker as column, Close price as values
#print(daily_close_px)
daily_pct_change = daily_close_px.pct_change()

#Plot the distributions
daily_pct_change.hist(bins=50, sharex=True, figsize=(12,8))
#plt.show()
pd.scatter_matrix(daily_pct_change, diagonal='kde', alpha=0.1, figsize=(12,12))
plt.show()
min_periods = 75
vola = daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods) # Calculate the volatility
vola.plot(figsize=(10,8),title='Volatility')
plt.show()