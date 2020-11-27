import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import numpy as np
#mport statsmodels.api as sm
from matplotlib.widgets import MultiCursor

def trend(df):
    signals = pd.DataFrame(index=df.index)
    signals['MACDTrendSignal'] = 0
    signals['MACDTrendSignal'][26:] = np.where(df['MACD'][26:] >= df['Signal'][26:],1,0)
    signals['action'] = signals['MACDTrendSignal'].diff()
    signals['MACD']=df['MACD']
    print('MACD is: \n',signals.MACD)
    fignew = plt.figure()
    ax1 = fignew.add_subplot(211)
    df['MACD'].plot(ax=ax1, color='m',marker='o')
    df['Signal'].plot(ax=ax1, color='y')
    ax1.plot(signals.loc[signals.action == 1.0].index, signals.MACD[signals.action == 1.0],'^', markersize=10, color='g')
    ax1.plot(signals.loc[signals.action == -1.0].index, signals.MACD[signals.action == -1.0],'v', markersize=10, color='r')
    ax2=fignew.add_subplot(212,sharex=ax1)
    df['Close'].plot(ax=ax2)
    multiC=MultiCursor(fignew.canvas,(ax1,ax2),lw=1)
    plt.show()
    return signals

def backtest(df, signals, initial_capital, stockname, share):
    positions = pd.DataFrame(index=df.index).fillna(0)
    positions[stockname] = share * signals['MACDTrendSignal'].fillna(0)
    portfolio = positions.multiply(df['Close'], axis=0) #initialize the portfolio with value owned. df.multiply is pandas function to multiply 2 DFs axis=0 means to compare by index, axis =1 means compare by columns
    pos_diff = positions.diff().fillna(0)
    
    portfolio['holdings'] = (positions.multiply(df['Close'],axis=0)).sum(axis=1) #The sum() is applied on "positions" dataframe, not portfolio. add the columns of "positions" and store them in "portfolio"
    portfolio['cash']=initial_capital - (pos_diff.multiply(df['Close'],axis=0)).sum(axis=1).cumsum(axis='index')
    portfolio['total']=portfolio['cash']+portfolio['holdings']
    portfolio['returns']=portfolio['total'].pct_change().fillna(0)

    print('Portfolio new \n',portfolio)

    fig = plt.figure()
    fig.suptitle('Total Asset', fontsize=18)
    ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')
    portfolio['total'].plot(ax=ax1, lw=2.)
    ax1.plot(portfolio.loc[signals.action == 1.0].index, portfolio.total[signals.action==1.0],'^',markersize=10, color='g')
    ax1.plot(portfolio.loc[signals.action == -1.0].index, portfolio.total[signals.action==-1.0],'v',markersize=10, color='r')
    plt.show()

    ###### Calculate sharp ratio ##### the greater the ratio, the better. 1 is acceptable, 2 is very good, 3 is excellent
    returns=portfolio['returns']
    sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())
    print('The sharpe ratio of this strategy is: ', sharpe_ratio)

    ##### Maximum Drawdown ##### measure the largest single drop from peak to bottom. This indicates the risk of a portfolio
    window = 252
    rolling_max = df['Close'].rolling(window,min_periods=1).max()
    daily_drawdown = df['Close']/rolling_max - 1.0
    max_daily_drawdown = daily_drawdown.rolling(window,min_periods=1).min()
    fig_Drawdown = plt.figure()
    fig_Drawdown.suptitle('Maximum Draw Down', fontsize=18)
    daily_drawdown.plot()
    max_daily_drawdown.plot()

    plt.show()


    ##### Compound Annual Growth Rate #####
    days = (portfolio.index[-1]-portfolio.index[0]).days
    cagr = ((((portfolio['total'][-1]) / portfolio['total'][1])) ** (365.0/days)) - 1  # the ** operator means exponentiation. a**b means a hoch b
    print('The CAGR of this strategy is: ',cagr)

    return portfolio