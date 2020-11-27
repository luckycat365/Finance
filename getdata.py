import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import FinanceUtil as tool

#try11='haha'
#print('try character is {}'.format(try11))

style.use('ggplot')
name='NVDA'
start = dt.datetime(2010, 1, 11)
end = dt.datetime.now()
#df = web.DataReader(name, 'yahoo', start, end)


#-------------Get Multiple Stock info----------------------------
stocks = ['NVDA','AMD', 'PFE']
for stock in stocks:
    df = web.DataReader(stock, 'yahoo', start, end)
    df.to_csv('StockOfInterest/{}.csv'.format(stock))


#df=tool.gettickers(name,start,end)
#print(df)

#print(df['Open'].values)
#df.to_csv(name+'.csv')   #export data to csv file
#df.to_csv('stock_dfs/{}.csv'.format(name))

#df.reset_index(inplace=True)
#df.set_index("Date", inplace=True)
#df = df.drop("Symbol", axis=1)

#print(df.head())