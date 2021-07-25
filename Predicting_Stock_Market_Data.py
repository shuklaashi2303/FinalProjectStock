#!/usr/bin/env python
# coding: utf-8

# Import Depandencies for Data Extraction
import pandas as pd
import yfinance as yf
import datetime
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import password
import psycopg2

# Creating a Database Connection & Engine
DATABASE_CONNECTION = f"postgresql://postgres:{password}@127.0.0.1:5432/Portfolio"
engine = create_engine(DATABASE_CONNECTION)
session = Session(engine)

#Extracting Data from SQL
spxdata = db.MetaData()
spx_data = db.Table('spx500', spxdata, autoload=True, autoload_with=engine)
query = db.select([spx_data])
ResultProxy = session.execute(query)
ResultSet = ResultProxy.fetchall()

# Converting SQL Data to Pandas DataFrame
spx_data_df = pd.DataFrame(ResultSet)
spx_data_df.columns = ResultSet[0].keys()

# Defining Parametres for Main Data Frame 
Symbol_df = spx_data_df['symbol']
start = datetime.datetime.today()-datetime.timedelta(3650)
end = datetime.datetime.today()
cl_price = pd.DataFrame()
ohlcv_data = {}

# Data Extraction with YFinance API
for ticker in Symbol_df:
    cl_price[ticker] = yf.download(ticker, start, end)['Adj Close']

# Creating Main Data Frame for Machine Learning
Main_df = cl_price.dropna(axis = 1)
Stock_df = Main_df['MMM']
Stock_Data = Main_df['MMM'].reset_index()

# Import Dependancies for Data Preprocessing for Machine Learning
from sklearn.preprocessing import MinMaxScaler
import numpy as np
scaler=MinMaxScaler(feature_range=(0,1))
Stock_df1 = scaler.fit_transform(np.array(Stock_df).reshape(-1,1))
import plotly.express as px
import plotly.graph_objects as go

#Plot Current Stock Price
fig = px.line(Stock_Data, x="Date", y="MMM")

fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

fig.show()

##splitting dataset into train and test split
training_size=int(len(Stock_df1)*0.65)
test_size=len(Stock_df1)-training_size
train_data,test_data=Stock_df1[0:training_size,:],Stock_df1[training_size:len(Stock_df1),:1]
training_size,test_size

# Function for Creating Data Set Arrays 
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step), 0]  
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

# Creation of Testing & Training Data 
time_step = 100
X_train, y_train = create_dataset(train_data, time_step)
X_test, ytest = create_dataset(test_data, time_step)

# Reshaping Test-Train Data 
X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)

# Import Dependancies for Deep Learning
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
import math
from sklearn.metrics import mean_squared_error

# Adding Layers 
model=Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
model.add(LSTM(50,return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error',optimizer='adam')
model.summary()

# Data Fitting
model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=100,batch_size=64,verbose=1)

# Prediction and check performance metrics
train_predict=model.predict(X_train)
test_predict=model.predict(X_test)

# Transformback to original form
train_predict=scaler.inverse_transform(train_predict)
test_predict=scaler.inverse_transform(test_predict)

# Calculate RMSE performance metrics
math.sqrt(mean_squared_error(y_train,train_predict))

# Test Data RMSE
math.sqrt(mean_squared_error(ytest,test_predict))

# shift train predictions for plotting
look_back=100
trainPredictPlot = np.empty_like(Stock_df1)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(train_predict)+look_back, :] = train_predict
# shift test predictions for plotting
testPredictPlot = np.empty_like(Stock_df1)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(train_predict)+(look_back*2)+1:len(Stock_df1)-1, :] = test_predict

# Creating Data Frame for Plotting 
Stock = pd.DataFrame(scaler.inverse_transform(Stock_df1), columns = ['Stock Price'])
Test_Data = pd.DataFrame(data = testPredictPlot, columns = ['Test',]).dropna()
Training_Data = pd.DataFrame(trainPredictPlot, columns = ['Training']).dropna()
predection_df = pd.concat([Stock_Data['Date'], Stock, Test_Data, Training_Data], axis = 1)

# Testing vs Training Data
fig1 = px.line(predection_df, x="Date", y=["Test","Training"])

fig1.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

fig1.show()

