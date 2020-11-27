import csv
import pandas as pd
import numpy as np

def getTickerList(csvfile):
    
    df = pd.read_csv(csvfile)
    #if the source file is excel sheet, use df = pd.read_excel('filename.xlsx')
    df.set_index("Tickers", inplace=True)
    df['Cost'] = df['Amount'] * df['PricePerShare']
    print('Before: \n', df)
    df = df.sort_values(by=['Cost'])
    print('After: \n', df)
    return(df)