import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

import matplotlib.dates as mdates
from matplotlib.widgets import MultiCursor

#df['50ma']=df['Adj Close'].rolling(window=50).mean()   #calculate 100 day moving average and store in a new column "100ma"
#df_ohlc=df['Adj Close'].resample('10D').ohlc() #open high low close 10 days resample
def gettickers(tickers, startdate, enddate):
    def data(ticker):
        return (web.DataReader(ticker, 'yahoo', startdate, enddate))
    datas = map (data, tickers)
    return(pd.concat(datas, keys=tickers, names=['Ticker', 'Date']))

def transform_to_weekly_data(df):
    offset = pd.offsets.timedelta(days=-6) # this somehow helps resample to calculate the weekly charts based on first valid trading day and last valid trading day in a week
    logic = {'Open'  : 'first',
            'High'  : 'max',
            'Low'   : 'min',
            'Close' : 'last',
            'Volume': 'sum'}
    df_week=df.resample('W',loffset=offset).apply(logic) #just as df, here the Date is still used as index.
    #print (df.tail(20))
    #print (df_week.tail())
    return df_week 

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

def compute_SMA(df, *args):
    for e in args:
        df['{} avg'.format(str(e))] = df['Close'].rolling(window=e,min_periods=1).mean()
    #print(df.tail())
    return df

def bollinger(df,days):
    df['Bollinger avg'] = df['Close'].rolling(window=days,min_periods=1).mean()
    df['Bollinger Upper'] = df['Bollinger avg'] + 2*df['Close'].rolling(window=days,min_periods=1).std()
    df['Bollinger Lower'] = df['Bollinger avg'] - 2*df['Close'].rolling(window=days,min_periods=1).std()
    return df

def compute_RSI(df,rsi_period):
    change = df['Close'].diff(1)  #diff(1) is the same as diff()
    gain = change.mask(change<0, 0)
    loss = change.mask(change>0, 0)
    
    tempdf = pd.DataFrame(index=df.index)
    tempdf['gain']=gain
    tempdf['loss']=loss
    #tempdf['avg_gain'] = tempdf['gain'].rolling(window=rsi_period,min_periods=rsi_period-1).mean()
    #tempdf['avg_loss'] = tempdf['loss'].rolling(window=rsi_period,min_periods=rsi_period-1).mean()
    tempdf['avg_gain'] = tempdf['gain'].ewm(com=rsi_period-1,min_periods=rsi_period).mean()
    tempdf['avg_loss'] = tempdf['loss'].ewm(com=rsi_period-1,min_periods=rsi_period).mean()
    tempdf['rs'] = abs(tempdf['avg_gain'])/abs(tempdf['avg_loss'])
    df['RSI'] = 100-100/(1+tempdf['rs'])
    
    return df


def simple_visualization(df,name,result):
    from matplotlib.widgets import Cursor
    fig = plt.figure()
    fig.suptitle(name, fontsize=18)
    ax1=fig.add_subplot(311)
    ax1.plot(df.index, df['Close'],color='b',linewidth=2, marker='o',markersize=5)
    ax1.plot(df.index, df['Bollinger avg'],color='black',linewidth=0.5)
    ax1.plot(df.index, df['Bollinger Upper'],color='r',linewidth=0.5)
    ax1.plot(df.index, df['Bollinger Lower'],color='g',linewidth=0.5)
    #cursor = Cursor(ax1, useblit=True,color='blue', linewidth=2)
    ax1.fill_between(df.index, df['Bollinger Upper'], df['Bollinger Lower'], color='yellow')
    ax2=fig.add_subplot(312,sharex=ax1,facecolor='grey',title='MACD')
    ax2.plot(df.index, df['MACD'],color='m')
    ax2.plot(df.index, df['Signal'], color='y')
    handles,label=ax2.get_legend_handles_labels()
    ax2.legend(handles,label,loc='lower right', fancybox=True, shadow=True)
    ax2.bar(df.index, df['MACD Histogram'],color='b')
    ax3=fig.add_subplot(313,sharex=ax1,title='RSI')
    ax3.plot(df.index, df['RSI'])
    thresh = pd.DataFrame(index=df.index)
    thresh['Overbought']=70
    thresh['Oversold']=30
    ax3.plot(df.index, thresh['Overbought'], '--',  color='red')
    ax3.plot(df.index, thresh['Oversold'],  '--',  color='green')
    multiC=MultiCursor(fig.canvas,(ax1,ax2,ax3),lw=1)
    plt.show()


def visualization_with_Candle(df,name,TP):
    from mpl_finance import candlestick_ohlc
    

    df_ohlc_DateAsColumn = df.reset_index(inplace=False) #make Date to a normal column, add new index incrementing from 0,because we need to access Date values for candlestick function
    df_ohlc_DateAsColumn['Date'] = df_ohlc_DateAsColumn['Date'].map(mdates.date2num)
    df_ohlc_drawCandle=df_ohlc_DateAsColumn[['Date','Open','High','Low','Close']].copy() #create required data in a new DataFrame for drawing Candlestick diagram

    fig, (ax1,ax2,ax3) = plt.subplots(3)
    if TP == 'week':
        fig.suptitle('Weekly Chart of {}'.format(name))
        wide=2
    elif TP == 'day':
        fig.suptitle('Daily Chart of {}'.format(name))
        wide=0.3

    ax1=plt.subplot2grid((11,1),(0,0),rowspan=5,colspan=1)
    ax2=plt.subplot2grid((11,1),(6,0),rowspan=1,colspan=1, sharex=ax1)   #sharex means when zoomed, the ax2 will be zoomed the same as ax1
    ax3=plt.subplot2grid((11,1),(8,0),rowspan=5,colspan=1, sharex=ax1)
    ax1.xaxis_date()    
    candlestick_ohlc(ax1,df_ohlc_drawCandle.values,width=wide,colorup='g')
    ymin,ymax = ax1.get_ylim()
    ax1_1 = ax1.twinx()
    #ax1_1.xaxis_date()
    ax1_1.plot(df_ohlc_DateAsColumn['Date'], df_ohlc_DateAsColumn['10 avg'], color='y')
    ax1_1.set_ylim([ymin,ymax])
    ax1_2=ax1.twinx()
    ax1_2.plot(df_ohlc_DateAsColumn['Date'], df_ohlc_DateAsColumn['30 avg'], color='g')
    ax1_2.set_ylim([ymin,ymax])
    ax1_3=ax1.twinx()
    ax1_3.plot(df_ohlc_DateAsColumn['Date'], df_ohlc_DateAsColumn['72 avg'], color='b')
    ax1_3.set_ylim([ymin,ymax])
    ax1.set_ylabel('K Diagram', color='g')

    ax2.bar(df_ohlc_DateAsColumn['Date'],df_ohlc_DateAsColumn['Volume'])
    ax2.set_ylabel('Volumn',color='b')
    #ax2.fill_between(df_ohlc_DateAsColumn['Date'],df_ohlc_DateAsColumn['Volume'].values, 0)   # mdates is x, df_volume is y, from 0 to the y

    ax3.plot(df_ohlc_DateAsColumn['Date'], df_ohlc_DateAsColumn['MACD'],color='m')
    ax3.plot(df_ohlc_DateAsColumn['Date'], df_ohlc_DateAsColumn['Signal'],color='y')
    handles,label=ax3.get_legend_handles_labels()
    ax3.legend(handles,label,loc='lower right', fancybox=True, shadow=True)
    ax3_1 = ax3.twinx()
    ax3_1.bar(df_ohlc_DateAsColumn['Date'], df_ohlc_DateAsColumn['MACD Histogram'],color='b')
    
    ax3.set_ylabel('MACD',color='m')

    multiC=MultiCursor(fig.canvas,(ax1,ax2,ax3),lw=1)
    plt.show()

def appendStockname(df, stockname):
    df['Name']=stockname
    return df