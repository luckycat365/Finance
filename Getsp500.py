import bs4 as bs
import pickle
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker=row.findAll('td')[1].text
        tickers.append(ticker)

    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)   # dumping tickers to file f
    #print(tickers)
    return tickers

#save_sp500_tickers()




def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers=save_sp500_tickers()
    else: 
        with open("sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)
            print(tickers)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    start=dt.datetime(2010,1,1)
    end=dt.datetime.now()

    for ticker in tickers[291:399]:
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):  #check whether there is some csv file already in the path
            df=web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))


#get_data_from_yahoo()

#Now combine all stocks in 1 dataframe:
def compile_data():
    with open("sp500tickers.pickle","rb") as f:
        tickers = pickle.load(f)

    main_df=pd.DataFrame()
    for count,ticker in enumerate(tickers[:399]):
        df=pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)
        df.rename(columns={'Adj Close':ticker},inplace=True)
        df.drop(['Open','High','Low','Close','Volume'],1,inplace=True)

        if main_df.empty:
            main_df=df
        else:
            main_df=main_df.join(df, how='outer')

        if count%10==0:
            print(count)

    print(main_df.tail())
    main_df.to_csv('sp500_joined_closes.csv')

#compile_data()

def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv',parse_dates=True, index_col=0)
    print('shape of dataFrame is',df.shape)
    dfnew = df['AMD']
    dfnew.append(df['AMD'])
    #df['NVDA'].plot()
    #plt.show()
    #print(df.tail())
    df_corr = df.corr()
    #print(df_corr.head())

    data = df_corr.values
    print('shape of data is',data.shape)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)  #one by one, plot one
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap) #give you the legend
    ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)  #0.5 is the tick month
    ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels=df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)  #limit of the colors. -1 is min, 1 is max. This is according to the values in the corr map
    plt.tight_layout()
    plt.show()



visualize_data()
