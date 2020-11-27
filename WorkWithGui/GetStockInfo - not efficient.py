import csv
import pandas as pd
import numpy as np

def getTickerList(filepath):
    Listname =  filepath
    df = pd.DataFrame()
    with open(Listname, newline='') as f:
        myfile = csv.reader(f, delimiter=',')
        tickerlist=[]
        for row in myfile:
            if row[0] == "Tickers":
                labels = row
                labels 
                
                #print("new Labels: ", Reallabels, "new shape: ", Reallabels.shape)
            else:
                tickerlist = row
               
                
                
                #Realtickername = np.array(tickerlist[0])
                #print(Realtickername)
                Realtickerinfo = np.array(tickerlist, dtype='|S4, f4, f4, f4') # the default dimension is (4,1), pandas always needs (1,x) 
                Realtickerinfo = Realtickerinfo.reshape(1,4) # Reshape the array from (4,1) to (1,4) to meet pandas requirement
                #for i in range(1,4):
                 #   Realtickerinfo[0][i] = 3 #float(Realtickerinfo[0][i])
                  #  print("element",Realtickerinfo[0][i] )
                print("info: ",Realtickerinfo, "Shape: ", Realtickerinfo.shape)
                
                dfpart = pd.DataFrame(data=Realtickerinfo, columns=labels)
                dfpart = dfpart.set_index('Tickers')
                df = df.append(dfpart)
            
            #print("label: ", labels, '\n' "Tickers: ",tickerlist)
        test = df['Amount'].values * df['PricePerShare'].values
        print("Amount is: \n", df['Amount'])
        print("Price is: \n", df['PricePerShare'])
        print(test)
        df.to_csv("D:/Finance/Dataframe.csv")    
        #print("Dataframe is:",df)

    return(df)