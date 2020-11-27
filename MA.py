import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.widgets import MultiCursor
import pandas as pd
import pandas_datareader.data as web
import numpy as np

def expMA(values,window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a

def compute_MACD(df):
    nfast=12
    nslow=26 
    signalspan=9
    df['fastema'] = df['Close'].ewm(span=nfast, min_periods=1).mean()
    df['slowema'] = df['Close'].ewm(span=nslow, min_periods=1).mean()
    df['MACD'] = df['fastema'] - df['slowema']
    df['Signal'] = df['MACD'].ewm(span=signalspan, min_periods=1).mean()
    df['MACD Histogram'] = df['MACD'] - df['Signal']

    return df

    #result = pd.DataFrame({'MACD': emafast-emaslow, 'emaSlw': emaslow, 'emaFst': emafast})
    #return result

df=pd.read_csv('PFE.csv', parse_dates=True, index_col=0)  #parse_dates and index_col=0 are used to use dates as index
print(df.tail())
df['5ma']=df['Close'].rolling(window=5).mean()   #calculate 100 day moving average and store in a new column "100ma"
df['200ma']=df['Close'].rolling(window=200).mean()
df.dropna(inplace=True)  # drop the first 99 data because no 100 day moving average can be built, which are just Not-A-Number(NAN)
#df['100ma']=df['Adj Close'].rolling(window=100, min_periods=0).mean()    #Alternative to the 2 lines above, in the first 99 data, instead of building 100 MA, it build just the MA with what data history it has 
df['pct Change']=df['Close'].pct_change()
df=compute_MACD(df)
print(df.tail(30))
#print('ma',df['50ma'])
#print('ewm',fastema)
#print(df['12ema'].tail(5))
#df['Adj Close'].plot()
#plt.show()
#MACDFrame=moving_average_convergence(df['Adj Close'])
#df.append(MACDFrame)
#print("new \n",df.tail())
print('index',df.index)

fig, (ax1,ax2,ax3) = plt.subplots(3, sharex=True)
ax1=plt.subplot2grid((10,1),(0,0),rowspan=5,colspan=1)
ax2=plt.subplot2grid((10,1),(6,0),rowspan=1,colspan=1, sharex=ax1)   #sharex means when zoomed, the ax2 will be zoomed the same as ax1
ax3=plt.subplot2grid((10,1),(8,0),rowspan=2,colspan=1, sharex=ax1)
ax1.plot(df.index,df['Close'])
ax1.plot(df.index,df['5ma'])
#ax1.plot(df.index,df['200ma'])
#cursor = Cursor(ax1, useblit=True, color='red', linewidth=2)
multiC=MultiCursor(fig.canvas,(ax1,ax2,ax3),lw=1)
ax2.bar(df.index, df['Volume'])
ax2.set_ylabel('Trade Volume')
ax3.plot(df.index, df['MACD'],color='m')
ax3.plot(df.index, df['Signal'],color='y')
ax3.set_ylabel('MACD', color='m')
handles,labels = ax3.get_legend_handles_labels()
ax3.legend(handles,labels,loc='upper left', bbox_to_anchor=(0, 1.2),fancybox=True, shadow=True)
ax4 = ax3.twinx()  # instantiate a second axes in the same sub-diagram that shares the same x-axis with ax3
ax4.bar(df.index, df['MACD Histogram'], color='b')
ax4.set_ylabel('Histogram',color='b')

plt.show()