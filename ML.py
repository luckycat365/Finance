from collections import Counter
import numpy as np
import pandas as pd
import pickle
from sklearn import svm,  neighbors
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
import keras
from keras.models import Sequential
from keras.layers import Dense

def process_data_for_labels(ticker):
    hm_days=7
    df = pd.read_csv('sp500_joined_closes.csv',parse_dates=True, index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1, hm_days+1):
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker])/df[ticker]  #(future i Day value - today's value)/today's value

    df.fillna(0,inplace=True)
    print(df.tail(10))
    return tickers, df

#process_data_for_labels('PFE')

def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.03
    for col in cols:
        if col > requirement:
            return 1
        elif col < -requirement:
            return -1
    return 0

def extract_featuresets(ticker):
    tickers, df=process_data_for_labels(ticker)

    df['{}_target'.format(ticker)] = list(map(buy_sell_hold, 
                                              df['{}_1d'.format(ticker)],
                                              df['{}_2d'.format(ticker)],
                                              df['{}_3d'.format(ticker)],
                                              df['{}_4d'.format(ticker)],
                                              df['{}_5d'.format(ticker)],
                                              df['{}_6d'.format(ticker)],
                                              df['{}_7d'.format(ticker)]))

    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread:',Counter(str_vals))

    df.fillna(0,inplace=True)  #replace NAN by 0
    df = df.replace([np.inf, -np.inf], np.nan)  # adress preis change from 0 to any number, deviding by 0 gives you inf
    df.dropna(inplace=True)

    df_vals=df[[ticker for ticker in tickers]].pct_change()
    df_vals=df.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)

    X = df_vals.values # Feature set
    y = df['{}_target'.format(ticker)].values # label set
    print("size of X:",X.shape)
    #print("size of y:",y.shape)
    return X,y,df

#extract_featuresets('NVDA')

def do_ML(ticker):
    X,y,df = extract_featuresets(ticker)
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25)

    #clf = neighbors.KNeighborsClassifier()
    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier())])

    clf.fit(X_train,y_train)
    confidence = clf.score(X_test,y_test)
    print('Accuracy',confidence)
    predictions = clf.predict(X_test)
    print('Predicted spread:', Counter(predictions))

    return confidence


def do_DL(ticker):
    X,y,df=extract_featuresets(ticker)
    X_train,  X_test, y_train, y_test = train_test_split(X,y,test_size=0.25)
    
    y_train = keras.utils.to_categorical(y_train,3)
    y_test = keras.utils.to_categorical(y_test,3)
    print('cat:',y_train)

    model = Sequential()
    model.add(Dense(128 , input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(64 , activation='relu'))
    model.add(Dense(3, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    model.fit(X_train,y_train,batch_size=64,epochs=10, verbose=1, validation_data=(X_test,y_test))
    weights, biases = model.layers[0].get_weights()
    print ('Weights layer 0 are:',weights)
    print('Biases layer 0 are:', biases)
    score=model.evaluate(X_test,y_test)
    print("Score is: ", score)
    result = model.predict(X_test)
    finalresult = []
    howmany = result.shape[0]
    print('shape:',result.shape[0])
    for i in range (howmany):
        maxvalue=np.amax(result[i])
        maxindex=np.where(result[i]==maxvalue)
  
        if maxindex[0][0] == 0:
            finalresult.append(-1)
        elif maxindex[0][0] == 1:
            finalresult.append(0)
        elif maxindex[0][0] == 2:
            finalresult.append(1)
    #print('Numbers:', result.shape)
    print('Predicted size:', len(finalresult))
    print('Predicted spread:', Counter(finalresult))

#do_ML('NVDA')
do_DL('NVDA')