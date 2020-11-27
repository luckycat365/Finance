import tkinter as tki

import GetStockInfo 
import matplotlib.pyplot as plt
import getdata
import FinanceUtil2020 as tool
import TechAnalysis as ta
import pandas as pd

portfoliopath = "K:/Finance/Portfolio.csv"
valuetodaypath = 'K:/Finance/WorkWithGui/PortfolioInfo/pricelisttoday.csv'
def main():
    
    startgui()

def getstockprice():      
    df=GetStockInfo.getTickerList(portfoliopath)
    Tickers = df.index.values
    pricetoday=getdata.getdatafromYahooToday(Tickers)
    dfwithvalue = tool.CalcValueToday(df,pricetoday)
    dfwithvalue.to_csv(valuetodaypath)
        
def showportfolio():
    dfwithvalue = pd.read_csv(valuetodaypath,index_col=0)
    TotalCost = dfwithvalue['Cost'].sum()
    Totalvaluetoday = dfwithvalue['ValueToday'].sum()
    TotalGrowth = (Totalvaluetoday - TotalCost)/TotalCost
    fig = plt.figure(figsize=[10,10])
    fig.suptitle("Cost: {}".format(TotalCost), fontsize=18)
    ax1=plt.subplot()
    ax1.pie(dfwithvalue['Cost'],labels=dfwithvalue.index, autopct = '%.1f%%', startangle=90)
    fig2 = plt.figure(figsize=[10,10])
    fig2.suptitle("ValueToday: {0}\n Growth: {1:.2%}".format(Totalvaluetoday, TotalGrowth), fontsize=18)
    ax2=plt.subplot()
    ax2.pie(dfwithvalue['ValueToday'],labels=dfwithvalue.index, autopct = '%.1f%%', startangle=90)
    #print("Growth: {:.2%}".format(TotalGrowth))
    plt.show()    


def startgui():
    def showtechchart():
        averagecount1 = 10
        averagecount2 = 30
        averagecount3 = 72
        BollingerDays = 20
        rsi_period = 14
        drawdiagram = True
        showlastXdays = 5
        TP = 'day'  # either week or day
        stockname = input1.get()
        dfhist = getdata.gethistdatafromYahoo(stockname)
        dfhist = tool.compute_RSI(dfhist, rsi_period)
        dfhist = tool.compute_MACD(dfhist)
        dfhist = tool.compute_SMA(dfhist, averagecount1, averagecount2, averagecount3)
        dfhist = tool.bollinger(dfhist, BollingerDays)
        result = ta.Technician(dfhist, stockname, False)
        result = tool.appendStockname(result, stockname)
        input1.delete(0,tki.END)
        tool.simple_visualization(dfhist,stockname,result)
        tool.visualization_with_Candle(dfhist,stockname, TP)

    window = tki.Tk()
    window.geometry('800x500')
    window.title('Vince Financial Analytic')
    lbl1 = tki.Label(window, text='Welcome to my Financial World', font=("Arial Bold",20),bg="Green",fg="Blue")
    lbl1.grid(column=0, row=0, columnspan=5)
    btn1 = tki.Button(window, text="Get Stock Price", font=("Arial",15), command = getstockprice)
    btn1.grid(column=0, row=2)
    btn2 = tki.Button(window, text="Show Portfolio", font=("Arial",15), command=showportfolio)
    btn2.grid(column = 0, row=4)

    lbl2 = tki.Label(window, text='Which Stock do you want to analize?', font=("Arial",15),fg="Blue")
    lbl2.grid(column=0, row=8, columnspan=5)
    input1 = tki.Entry(window)
    input1.grid(column=0, row=9)
    btn3 = tki.Button(window, text="Show Tech Chart", font=("Arial",15), command=showtechchart)
    btn3.grid(column=0, row=10)
    

    window.mainloop()







if __name__ == "__main__":
    main()