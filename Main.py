import pandas as pd
import pandas_datareader.data as web
import FinanceUtil as tool
import Strategy 
import TechAnalysis as ta
import datetime as dt



stockname = 'NVDA'
#df=pd.read_csv('{}.csv'.format(stockname), parse_dates=True, index_col=0)  #parse_dates and index_col=0 are used to use dates as index
start = dt.datetime(2011,1,2)
end = dt.datetime.now()
df = web.DataReader(stockname,'yahoo', start, end)


df=df[pd.Timestamp('2016-02-11'):] # Only take the values after 2016-02-11
#print('df \n',df.head())
TP = 'day'  # either week or day
initial_capital = float(2000.0)
share = 100


averagecount1 = 10
averagecount2 = 30
averagecount3 = 72

BollingerDays = 20
rsi_period = 14


if TP == 'week':
    df = tool.transform_to_weekly_data(df)

df=tool.compute_RSI(df, rsi_period)
df=tool.compute_MACD(df)
df=tool.compute_SMA(df, averagecount1,averagecount2,averagecount3)
df=tool.bollinger(df,BollingerDays)
result = ta.Technician(df)
# print('new\n',df.tail(50))
#signals = Strategy.trend(df)

#portfolio = Strategy.backtest(df, signals, initial_capital, stockname, share)


tool.simple_visualization(df,stockname,result)

#tool.visualization_with_Candle(df,stockname, TP)


    