import pandas as pd
import pandas_datareader.data as web
import FinanceUtil as tool
import Strategy 
import TechAnalysis as ta
import datetime as dt

start = dt.datetime(2016,1,2)
end = dt.datetime.now()
stocks = ['GOOG','T','CAT','ERIC','NOK','QCOM','VZ']
ObserveStocks = ['NVDA','JNJ','TSM','CSCO','IBM', 'MSFT', 'AMZN']
TP = 'day'  # either week or day
initial_capital = float(2000.0)
share = 100


averagecount1 = 10
averagecount2 = 30
averagecount3 = 72

BollingerDays = 20
rsi_period = 14
drawdiagram = False
showlastXdays = 5

overview =pd.DataFrame()
Observeoverview = pd.DataFrame()


for stockname in stocks:
    df = web.DataReader(stockname, 'yahoo', start, end)
    df.to_csv('D:/Finance/StockOfInterest/{}.csv'.format(stockname))


    df=pd.read_csv('D:/Finance/StockOfInterest/{}.csv'.format(stockname), parse_dates=True, index_col=0)  #parse_dates and index_col=0 are used to use dates as index



    #df=df[pd.Timestamp('2016-02-11'):] # Only take the values after 2016-02-11




    if TP == 'week':
        df = tool.transform_to_weekly_data(df)

    df=tool.compute_RSI(df, rsi_period)
    df=tool.compute_MACD(df)
    df=tool.compute_SMA(df, averagecount1,averagecount2,averagecount3)
    df=tool.bollinger(df,BollingerDays)
    result = ta.Technician(df,stockname, drawdiagram)
    result = tool.appendStockname(result,stockname)
    result_lastXdays = result.tail(showlastXdays)
    result_lastXdays.to_csv('D:/Finance/EvaluateStocks/{}_result_lastXdays.csv'.format(stockname))
    overview = overview.append(result_lastXdays)
    
    # print('new\n',df.tail(50))
    #signals = Strategy.trend(df)

    #portfolio = Strategy.backtest(df, signals, initial_capital, stockname, share)

    if drawdiagram == True:
        tool.simple_visualization(df,stockname,result)

        #tool.visualization_with_Candle(df,stockname, TP)
    overview.to_csv('D:/Finance/EvaluateStocks/All_result_last{}days.csv'.format(showlastXdays))


for observename in ObserveStocks:
    df2 = web.DataReader(observename, 'yahoo', start, end)
    df2.to_csv('D:/Finance/StockOfInterest/{}.csv'.format(observename))


    df2=pd.read_csv('D:/Finance/StockOfInterest/{}.csv'.format(observename), parse_dates=True, index_col=0)  #parse_dates and index_col=0 are used to use dates as index



    #df2=df2[pd.Timestamp('2016-02-11'):] # Only take the values after 2016-02-11




    if TP == 'week':
        df2 = tool.transform_to_weekly_data(df2)

    df2=tool.compute_RSI(df2, rsi_period)
    df2=tool.compute_MACD(df2)
    df2=tool.compute_SMA(df2, averagecount1,averagecount2,averagecount3)
    df2=tool.bollinger(df2,BollingerDays)
    result = ta.Technician(df2,observename, drawdiagram)
    result = tool.appendStockname(result,observename)
    result_lastXdays = result.tail(showlastXdays)
    result_lastXdays.to_csv('D:/Finance/EvaluateStocks/{}_result_lastXdays.csv'.format(observename))
    Observeoverview = Observeoverview.append(result_lastXdays)
    
    # print('new\n',df2.tail(50))
    #signals = Strategy.trend(df2)

    #portfolio = Strategy.backtest(df2, signals, initial_capital, observename, share)

    if drawdiagram == True:
        tool.simple_visualization(df2,observename,result)

        #tool.visualization_with_Candle(df2,stockname, TP)
    Observeoverview.to_csv('D:/Finance/EvaluateStocks/All_Observe_result_last{}days.csv'.format(showlastXdays))