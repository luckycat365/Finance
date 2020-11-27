
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import FinanceUtil2020 as tool
from matplotlib.widgets import Cursor
from matplotlib.widgets import MultiCursor


def Technician(df,stockname,drawdiagram):
    result = pd.DataFrame(index=df.index)
    result['Close']=df['Close']
    sellsymbol = -100
    strongsellsymbol = -200
    buysymbol = 100
    strongbuysymbol = 200

    #------Bollinger Band Analysis------1 means buy, 2 means strong buy, -1 means sell, -2 means strong sell-------
    result['Bollinger_Signal']=0
    distance=df['Bollinger Upper']-df['Bollinger Lower']
    #result['B-Overbuy']=df['Bollinger Upper']-distance*0.05
    #result['B-DOverbuy']=df['Bollinger Upper']+distance*0.1
    #result['B-Oversell']=df['Bollinger Lower']+distance*0.05
    #result['B-DOversell']=df['Bollinger Lower']-distance*0.1
    #print(distance.tail(50))
    result['Bollinger_Signal']=np.where(result['Close']>=df['Bollinger Upper']-distance*0.07,sellsymbol,result['Bollinger_Signal'])
    result['Bollinger_Signal']=np.where(result['Close']>=df['Bollinger Upper']+distance*0.1,strongsellsymbol,result['Bollinger_Signal'])
    result['Bollinger_Signal']=np.where(result['Close']<=df['Bollinger Lower']+distance*0.07,buysymbol,result['Bollinger_Signal'])
    result['Bollinger_Signal']=np.where(result['Close']<=df['Bollinger Lower']-distance*0.1,strongbuysymbol,result['Bollinger_Signal'])


    #fig=plt.figure()
    #ax1=fig.add_subplot(111)
    #result['Close'].plot(ax=ax1)
    ##result['B-Overbuy'].plot(ax=ax1, color='red',linewidth=0.5)
    ##result['B-DOversell'].plot(ax=ax1, color='black',linewidth=0.5)
    ##result['B-Oversell'].plot(ax=ax1, color='green',linewidth=0.5)
    #ax1.plot(result.loc[result.Bollinger_Signal == buysymbol].index, result.Close[result.Bollinger_Signal == buysymbol], '^', markersize=10, color='m')
    #ax1.plot(result.loc[result.Bollinger_Signal == 2].index, result.Close[result.Bollinger_Signal == 2], '^', markersize=10, color='g')
    #ax1.plot(result.loc[result.Bollinger_Signal == sellsymbol].index, result.Close[result.Bollinger_Signal == sellsymbol], 'v', markersize=10, color='black')
    #ax1.plot(result.loc[result.Bollinger_Signal == strongsellsymbol].index, result.Close[result.Bollinger_Signal == strongsellsymbol], 'v', markersize=10, color='red')
    #cursor = Cursor(ax1, useblit=True,color='blue', linewidth=2)
    #plt.show()
    #--------------------RSI Analysis-----------------------------------------------------------------------
    overbuy = 63
    strong_overbuy = 75
    oversold = 37
    strong_oversold = 25
    
    result['RSI_Signal']=0
    result['RSI']=df['RSI']
    result['RSI_Signal'] = np.where(df['RSI']>=overbuy,sellsymbol,result['RSI_Signal'])
    result['RSI_Signal'] = np.where(df['RSI']<=oversold,buysymbol,result['RSI_Signal'])
    result['RSI_Signal'] = np.where(df['RSI']>=strong_overbuy,strongsellsymbol,result['RSI_Signal'])
    result['RSI_Signal'] = np.where(df['RSI']<=strong_oversold,strongbuysymbol,result['RSI_Signal'])
    
    #----------------------Bollinger + RSI + RSI Gradient--------------------------------------------------------------
    result['Bollinger_RSI_Signal']=0
    rsi_gradient = np.gradient(result['RSI'].values)
    result['rsi_gradient'] = rsi_gradient
    result['Bollinger_RSI_Signal'] = np.where((result['RSI_Signal']<0) & (result['Bollinger_Signal']<0) & (result['rsi_gradient']<-1), sellsymbol, result['Bollinger_RSI_Signal'])
    result['Bollinger_RSI_Signal'] = np.where((result['RSI_Signal']>0) & (result['Bollinger_Signal']>0) & (result['rsi_gradient']>1), buysymbol, result['Bollinger_RSI_Signal'])
    result.drop(columns='RSI',inplace=True)

    if drawdiagram == True:
        fig=plt.figure()
        fig.suptitle(stockname,fontsize=18)
        ax1=fig.add_subplot(211)
        result['Close'].plot(ax=ax1)
        #result['B-Overbuy'].plot(ax=ax1, color='red',linewidth=0.5)
        #result['B-DOversell'].plot(ax=ax1, color='black',linewidth=0.5)
        #result['B-Oversell'].plot(ax=ax1, color='green',linewidth=0.5)
        ax1.plot(result.loc[result.Bollinger_RSI_Signal == buysymbol].index, result.Close[result.Bollinger_RSI_Signal == buysymbol], '^', markersize=10, color='m')
        #ax1.plot(result.loc[result.Bollinger_Signal == 2].index, result.Close[result.Bollinger_Signal == 2], '^', markersize=10, color='g')
        ax1.plot(result.loc[result.Bollinger_RSI_Signal == sellsymbol].index, result.Close[result.Bollinger_RSI_Signal == sellsymbol], 'v', markersize=10, color='black')
        #ax1.plot(result.loc[result.Bollinger_Signal == strongsellsymbol].index, result.Close[result.Bollinger_Signal == strongsellsymbol], 'v', markersize=10, color='red')
        result['temp']=0
        ax2=fig.add_subplot(212,sharex=ax1,title='RSI')
        ax2.plot(df.index, df['RSI'], marker='o', markersize=5)
        ax2.plot(df.index, result['rsi_gradient'], '*', markersize=1, color='red')
        ax2.plot(df.index, result['temp'], color='grey', linewidth=0.5 )
        thresh = pd.DataFrame(index=df.index)
        thresh['Overbought']=70
        thresh['Oversold']=30
        ax2.plot(df.index, thresh['Overbought'], '--',  color='red')
        ax2.plot(df.index, thresh['Oversold'],  '--',  color='green')
        multiC=MultiCursor(fig.canvas,(ax1,ax2),lw=1)
        plt.show()
        result.drop(columns=['temp'],inplace=True)


    #--------------------MACD Analysis-----------------------------------------------------------------------
    result['MACDTrendSignal'] = 0
    #result['MACD']=df['MACD']
    #result['Signal']=df['Signal']
    result['MACDTrendSignal'][26:] = np.where(df['MACD'][26:] >= df['Signal'][26:],100,0)
    result['MACD_Signal'] = result['MACDTrendSignal'].diff()
    result.drop(columns='MACDTrendSignal',inplace=True)
    
    #result['MACD']=df['MACD']
    #fignew = plt.figure()
    #ax1 = fignew.add_subplot(211)
    #df['MACD'].plot(ax=ax1, color='m',marker='o')
    #df['Signal'].plot(ax=ax1, color='y')
    #ax1.bar(df.index,df['MACD Histogram'])
    #ax1.plot(result.loc[result.MACD_Signal == 1.0].index, result.MACD[result.MACD_Signal == 1.0],'^', markersize=10, color='g')
    #ax1.plot(result.loc[result.MACD_Signal == -1.0].index, result.MACD[result.MACD_Signal == -1.0],'v', markersize=10, color='r')
    #ax2=fignew.add_subplot(212,sharex=ax1)
    #df['Close'].plot(ax=ax2)
    #multiC=MultiCursor(fignew.canvas,(ax1,ax2),lw=1)
    #plt.show()

    #------------------RSI + MACD-----------------------------------------------------------------------
    result['RSI_MACD_Signal'] = 0
    result['RSI_MACD_Signal'] = np.where((result['RSI_Signal']<0) & (result['MACD_Signal']<0), sellsymbol, result['RSI_MACD_Signal'])
    result['RSI_MACD_Signal'] = np.where((result['RSI_Signal']>0) & (result['MACD_Signal']>0), buysymbol, result['RSI_MACD_Signal'])
    

    #result.to_csv('try.csv')
    #result['MACD']=df['MACD']
    #fignew = plt.figure()
    #ax1 = fignew.add_subplot(311)
    #df['MACD'].plot(ax=ax1, color='m',marker='o')
    #df['Signal'].plot(ax=ax1, color='y')
    #ax1.bar(df.index,df['MACD Histogram'])
    #ax1.plot(result.loc[result.RSI_MACD_Signal == 1.0].index, result.MACD[result.RSI_MACD_Signal == 1.0],'^', markersize=10, color='g')
    #ax1.plot(result.loc[result.RSI_MACD_Signal == -1.0].index, result.MACD[result.RSI_MACD_Signal == -1.0],'v', markersize=10, color='r')
    #ax2=fignew.add_subplot(312,sharex=ax1,title='Price')
    #df['Close'].plot(ax=ax2)
    #ax2.plot(result.loc[result.RSI_MACD_Signal == 1.0].index, result.Close[result.RSI_MACD_Signal == 1.0],'^', markersize=10, color='g')
    #ax2.plot(result.loc[result.RSI_MACD_Signal == -1.0].index, result.Close[result.RSI_MACD_Signal == -1.0],'v', markersize=10, color='r')
    #ax3=fignew.add_subplot(313,sharex=ax1,title='RSI')
    #ax3.plot(df.index, df['RSI'])
    #thresh = pd.DataFrame(index=df.index)
    #thresh['Overbought']=70
    #thresh['Oversold']=30
    #ax3.plot(df.index, thresh['Overbought'], '--',  color='red')
    #ax3.plot(df.index, thresh['Oversold'],  '--',  color='green')
    #result.drop(columns='MACD',inplace=True)
    #multiC=MultiCursor(fignew.canvas,(ax1,ax2,ax3),lw=1)
    #plt.show()

    



    #-------------------Export results and return value---------------------------------------
    #result.drop(columns=['Close'],inplace=True)
    result.drop(columns='rsi_gradient', inplace=True)
    
    print(result.tail(3))
    return result