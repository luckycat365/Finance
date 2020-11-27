import GetStockInfo 
import matplotlib.pyplot as plt
import getdata
import FinanceUtil2020 as tool
import TechAnalysis as ta


def main():
    print("Yeah")
    #------------------Portfolio Info----------------------
    filepath = "K:/Finance/Portfolio.csv"
    df=GetStockInfo.getTickerList(filepath)
    Tickers = df.index.values
    #print("Dataframe is: \n", df)
    #print("Tickers are:", Tickers)

    pricetoday=getdata.getdatafromYahooToday(Tickers)
    dfwithvalue = tool.CalcValueToday(df,pricetoday)

    TotalCost = dfwithvalue['Cost'].sum()
    Totalvaluetoday = dfwithvalue['ValueToday'].sum()
    TotalGrowth = (Totalvaluetoday - TotalCost)/TotalCost
    fig = plt.figure(figsize=[10,10])
    fig.suptitle("Cost: {}".format(TotalCost), fontsize=18)
    ax1=plt.subplot()
    ax1.pie(df['Cost'],labels=df.index, autopct = '%.1f%%', startangle=90)
    fig2 = plt.figure(figsize=[10,10])
    fig2.suptitle("ValueToday: {0}\n Growth: {1:.2%}".format(Totalvaluetoday, TotalGrowth), fontsize=18)
    ax2=plt.subplot()
    ax2.pie(dfwithvalue['ValueToday'],labels=df.index, autopct = '%.1f%%', startangle=90)
    #print("Growth: {:.2%}".format(TotalGrowth))
    plt.show()

    #-------------Analyze single Stock----------------------
    averagecount1 = 10
    averagecount2 = 30
    averagecount3 = 72
    BollingerDays = 20
    rsi_period = 14
    drawdiagram = True
    showlastXdays = 5
    TP = 'day'  # either week or day

    stockname = input("Which Stock do you want to evaluate?")
    dfhist = getdata.gethistdatafromYahoo(stockname)
    dfhist = tool.compute_RSI(dfhist, rsi_period)
    dfhist = tool.compute_MACD(dfhist)
    dfhist = tool.compute_SMA(dfhist, averagecount1, averagecount2, averagecount3)
    dfhist = tool.bollinger(dfhist, BollingerDays)
    result = ta.Technician(dfhist, stockname, False)
    result = tool.appendStockname(result, stockname)
    if drawdiagram == True:
        tool.simple_visualization(dfhist,stockname,result)

        #tool.visualization_with_Candle(dfhist,stockname, TP)

if __name__ == "__main__":
    main()