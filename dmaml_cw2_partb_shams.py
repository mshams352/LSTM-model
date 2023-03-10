# -*- coding: utf-8 -*-
"""DMAML_CW2_PartB_Shams.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nykNGj57dWeyUOeFHAYQVPen3aRpN_r3

Import the necessary libraries
"""

! pip install https://github.com/pandas-profiling/pandas-profiling/archive/master.zip

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn import preprocessing
import plotly.graph_objects as go
import pandas_profiling
from pandas_profiling import ProfileReport
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import tkinter
import seaborn as sns

"""Read the data with the help of pandas"""

Netflix_data = pd.read_csv('NFLX_24may2002to17apr2022.csv')

"""Preliminary parts to understand the data"""

Netflix_data.info()

print(Netflix_data.shape)

Netflix_data.head()

Netflix_data.dtypes

"""Understand the number of missing values in each column by the number of them and the percentage"""

Netflix_data.isna().sum()

"""Understand data in the table"""

Netflix_data.describe()

report = ProfileReport(Netflix_data, title='Pandas Profiling Report Task B dataset CW2', html={'style':{'full_width':True}})
report.to_file(output_file="CW2_DataB_statistics.html")

Netflix_data

"""Choose only the close column for our prediction"""

Netflix_data =  Netflix_data[['Date','Close']]
Netflix_data.head()

"""Visualize the data set"""

Netflix_data.Date=pd.to_datetime(Netflix_data.Date, format='%Y/%m/%d')
Netflix_data= Netflix_data.set_index('Date')

"""Define figure for the stock prize"""

plt.clf()
plt.plot(Netflix_data.loc['2021-04-16':'2022-04-17'])
plt.savefig('CW2_partB_fig.png', dpi=1050)
plt.show

"""fix random seed for reproducibility"""

np.random.seed(7)

Netflix_data.shape

"""Normalize the dataset"""

Netflix_data=Netflix_data.loc['2016-04-16':'2022-04-17']
scaler = MinMaxScaler(feature_range=(0, 1))
Netflix_data_for_LSTM = scaler.fit_transform(Netflix_data)
Netflix_data.shape

"""Split into train and test sets"""

train_size = int(len(Netflix_data_for_LSTM) * 0.70)
test_size = len(Netflix_data_for_LSTM) - train_size
train, test = Netflix_data_for_LSTM[0:train_size, :], Netflix_data_for_LSTM[train_size:len(Netflix_data_for_LSTM), :]
train.shape

test.shape

"""Convert an array of values into a dataset matrix"""

def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)


np.random.seed(7)

"""Reshape into X=t and Y=t+1"""

look_back = 1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)
print(trainX.shape)
print(trainY.shape)
print(testX.shape)
print(testY.shape)

"""Reshape input to be [samples, time steps, features]"""

trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

"""Create and fit the LSTM network"""

model = Sequential()
model.add(LSTM(5,input_shape=(1, look_back)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=2)

model.summary()

"""Make predictions"""

trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

"""Invert predictions"""

trainPredict=scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])

"""Calculate root mean squared error"""

trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
print('Train Score: %.2f RMSE' % trainScore)
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
print('Test Score: %.2f RMSE' % testScore)

"""Shift train predictions for plotting"""

trainPredictPlot = np.empty_like(Netflix_data_for_LSTM)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict

"""Shift test predictions for plotting"""

testPredictPlot = np.empty_like(Netflix_data_for_LSTM)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict) + (look_back * 2) + 1:len(Netflix_data_for_LSTM) - 1, :] = testPredict

"""Plot baseline and predictions"""

plt.clf()
plt.plot(scaler.inverse_transform(Netflix_data_for_LSTM))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()
plt.savefig('CW2_prediction.png', dpi=1050)

"""Prediction price and actual price in a data frame together"""

y_actual=np.append(trainY,testY)
y_predicted=np.append(trainPredict,testPredict)
results=pd.DataFrame()
results['Actual_value']=y_actual
results['Predicted_value']=y_predicted 
results