import datetime as dt
import pandas as pd
import pandas_datareader.data as web
#import FinanceUtil as tool

def getdatafromYahooToday(Tickers): #Get the price today of stocks and pack them into one dataframe

    start = dt.datetime(2020,1,2)
    end = dt.datetime.today()
    #-------------Get Multiple Stock info----------------------------
    stocks = Tickers
    dftoday = pd.DataFrame()
    for stock in stocks:
        dflong = web.DataReader(stock, 'yahoo', start, end)
        dftoday=dftoday.append(dflong[-1:])
        #print ("Frame is: ", df)
        #df.to_csv('PortfolioInfo/{}.csv'.format(stock))
    pricetoday = dftoday["Close"].values
    
    for i in range(0,len(pricetoday)):
        pricetoday[i] = round(pricetoday[i],2)
    
    #print ("Price today is: ", pricetoday)
    return pricetoday

def gethistdatafromYahoo(Ticker):
    start = dt.datetime(2019, 1, 2)
    end = dt.datetime.today()
    dfhist = web.DataReader(Ticker, 'yahoo', start, end)
    return dfhist