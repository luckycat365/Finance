import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import numpy as np
import statsmodels.api as sm

df=pd.read_csv('GOOG.csv', parse_dates=True, index_col=0)  #parse_dates and index_col=0 are used to use dates as index
#df = df.loc[pd.Timestamp('2018-1-12'):pd.Timestamp('2019-3-15')]
#print('index \n',df.index)
#print('column \n',df.columns)

#ts=df['Close'][-10:]
#print('type \n',type(ts))
#print(df.loc[pd.Timestamp('2010-1-12'):pd.Timestamp('2010-3-15')])

#sample = df.sample(20) #randomly sample the dataframe and get 20 rows
#print(sample)
print(df)

df['pct_change']=df['Close'].pct_change() #get percentage change of two following rows. The result is not in % unit, but absolute value: 0.02 means 2%, not 0.02%
df['cum_daily_return'] = (1+df['pct_change']).cumprod() #calculate accumulative return
#print('close value: \n',df['Close'].tail())
#print('accumulative return: \n', df['cum_daily_return'].tail())
df['cum_daily_return'].plot()
plt.show()

min_periods = 75
df['volatility'] = df['pct_change'].rolling(min_periods).std() * np.sqrt(min_periods) # Calculate the volatility
df['volatility'].plot(figsize=(10,8),title='Volatility')
plt.show()
#df['pct_change_new']=df['Close']/df['Close'].shift(1)-1
#print('second \n',df['pct_change_new'].tail())
df.fillna(0, inplace=True)
#print(df.head())
df['log_return']=np.log(df['pct_change']+1)
#print(df['log_return'].tail())
#print(df['pct_change'].describe())
df['pct_change'].hist(bins=100)
plt.show()