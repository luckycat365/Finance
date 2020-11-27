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
print(df.tail())

df2=pd.read_csv('{}.csv'.format(stockname)) 
print(df2.tail())