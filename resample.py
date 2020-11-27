import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

df=pd.read_csv('PFE.csv', parse_dates=True, index_col=0)  #parse_dates and index_col=0 are used to use dates as index
#df['50ma']=df['Adj Close'].rolling(window=50).mean()   #calculate 100 day moving average and store in a new column "100ma"
#df_ohlc=df['Adj Close'].resample('10D').ohlc() #open high low close 10 days resample
offset = pd.offsets.timedelta(days=-6) # this somehow helps resample to calculate the weekly charts based on first valid trading day and last valid trading day in a week
logic = {'Open'  : 'first',
         'High'  : 'max',
         'Low'   : 'min',
         'Close' : 'last',
         'Volume': 'sum'}
df_ohlc_Dateindex=df.resample('W',loffset=offset).apply(logic)
print('origin \n',df.tail(20))
#print('after resample \n',df_ohlc.tail())

df_ohlc=df_ohlc_Dateindex.reset_index(inplace=False)
print('keep \n',df_ohlc_Dateindex.tail())
print('new \n',df_ohlc.tail())
df_ohlc.reset_index(inplace=True) # Date was used as index, now we add new index to this dataframe and make Date to a normal column, because we need to access Date values for candlestick function
#print(df_ohlc)
#df_ohlc['Date'] = pd.to_datetime(df_ohlc['Date'])
#df_ohlc['Date'] = df_ohlc['Date'].apply(mdates.date2num)
df_ohlc['Date']=df_ohlc['Date'].map(mdates.date2num)
df_ohlc_newframe=df_ohlc[['Date','Open','High','Low','Close']].copy() #create required data in a new DataFrame
#df_volume=df['Volume'].resample('10D').sum() #sum 10 days resample


#df_ohlc.reset_index(inplace=True)
#print("new:\n",df_ohlc.tail())

#df_ohlc['Date']=df_ohlc['Date'].map(mdates.date2num)
#print("new2:\n",df_ohlc.tail())

ax1=plt.subplot2grid((8,1),(0,0),rowspan=5,colspan=1)
ax2=plt.subplot2grid((8,1),(7,0),rowspan=1,colspan=1, sharex=ax1)   #sharex means when zoomed, the ax2 will be zoomed the same as ax1
ax1.xaxis_date()
candlestick_ohlc(ax1,df_ohlc_newframe.values,width=2,colorup='g')
#ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values, 0)  # mdates is x, df_volume is y, from 0 to the y

ax2.fill_between(df_ohlc_Dateindex.index,df_ohlc['Volume'].values, 0)

plt.show()