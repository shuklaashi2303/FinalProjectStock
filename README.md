![images](https://user-images.githubusercontent.com/79673185/126924525-8ead7039-b6dd-4469-8c71-83ec00f70d9a.jpeg)

## Topic: Stock Analysis

## QUESTION:
- Can a client's profile predict successful/growth in stock investment? 

## Factors and stocks we are going to work
- We are using S&P 500 stocks data where we have extracted the csv file using yfinance API to pgadmin called constituents.csv
-

## Reason Why Topic Was Chosen:
- The group has a shared interest of stock market, investment and finance. 
- Stock Analysis is a hot topic and in high demand 
- Has Machine Learning potential

## Description of Data Source: 
- Data is gathered from yahoo finance and saved into csv file called constituents.csv
- constituents.csv dataset has three columns such as Symbol, Name & Sector. It also has 506 rows
- There are 506 stocks per company that fall under 11 sectors such as health care, real estate and etc.
- We used both stored and live data to conduct this research analysis
- Another source is to use finance using- pip install finance
- Exploratory Analysis is conducted and the details are in the folder with the same name
## Questions Hoping to Answer:
- What is the expected value of the customers' stocks based on their portfolio in the future? (prediction)
- What is the future value of the customers' stocks based on their current portfolio? (prediction)

## Means of Communication:
- We used office hours and class time on Tuesday and Thursday to discuss and divide the project work among five teammates.

- Communication method mostly used slack and zoom calls on weekends Friday and Saturday evenings.

## Data Visualizations:
- We are using finance as sample data to make the web page. The focus is to make the webpage using dash, poorly, py and heroic app. we need to create dropdown box as per different stocks to highlight the time frame analysis using graphs like line, candles.

- We are also making the dashboard in order to forecast the visualization process and how to use the  analysis to make interface for clients who can predict the portfolio growth by using the stocks that we have selected or client's has in it.

 visit http://127.0.0.1:8055/ in your web browser.
 
## Using Machine Learning to Predict Stock Data:

This project is purely for educational & research purposes and should not be considered as advice or endorsement for investing in any stocks used for this study. The stock market is a lucrative way to earn money in the long & short term. It is a gamble that can often lead to a profit or a loss. There is no proper prediction model for stock prices. The price movement is highly influenced by the demand and supply for a stcok at a given time. This is majorly due to the volatile nature of the market and how a new can influence a stock's price. This study aims at predicting stock data for the future using technical analysis. Technical analysis is a study which reinforces that history repeats itself and through this study, we are using past data to predict future data using machine learning.    

## Model Selection

We selected the regression model to predict our results. The dependant variable for our regression will be the expected future values while the independant variable will be the values of the past. Due to the large volume of data that we have, which is prices for the past 10 years for the 500 components of the infamous S&P 500 index, we have decided to use deep learning & nural networks to do our predictions.

## Data Preprocessing

The data that we have is for the this study is the closing prices for the past 10 years of every single constituent of the S&P 500 index. Stock prices are continuous in nature and follow a lognormal distribution. Stock returns follow a normal distribution and the data seems to portray a mean reverting value of the stock returns. For deriving the stock returns, we used the pct_change() function in Pandas to convert stock prices to stock returns. The sample stock that was selected for testing was MMM since the data had minimum volitility compared to peers. A pandas dataframe was created to house the MMM stock price data and MMM daily return data. These individual dataframes were then converted to a numpy array.

#### Feature Engineering

Features used for testing and training the data were the 10yrs worth of Stock Price for stock MMM and 10yrs worth of daily returns for MMM. For the stock price data, we used a min-max-scalar since the data is lognornal and has minimum & maximum values that can be used in the sequential & LSTM models. The stock returns data followed a normal distribution and appears to have a mean reverting property. Hence a Standard Scalar was used to predict the future returns. 

## Splitting Data for Testing & Training

After plotting the 10 year data for MMM, the stock price & stock returns seemed to be steady until 2016.After 2016, there were noticible big jumps in price & return volatility. Hence 65% of the data was used for testing and 34% of the data was used for training the model

## Benefits & Limitations of using Linear Regression Model

## Benefits
- The regression model is simple in nature and assumes a linear relationship.
- It works well irrespective of data size.
- It gives information about the relevance of features.
- The model is easy to interpret.

## Limitations
- Assumes a linear relationship which may not always be the case.
- Overfitting can easily occur witin the model.
- Produces poor results on small datasets.
- Often times generate a spourious relationship between variables.

## Model Training

The models whcih predict the stock prices & returs have been trained with nural networks. The sequential model is being used along with dense and LSTM layers from keras to train the model. Currently 50 layers are being used for training puropses. There will be ongoing tesing done by increaseing and decreasing the layers to determine what effect it will have on the results. We may also change the stock we are predicting from MMM to another stock to see if the results vary.

## Accuracy Scores

- RMSE :  The RMSE for the Stock prices tested in the min max scalar has a value of 171.01 while the RMSE for stock returns in the standard scalar has a value of 1.36
- Mean Absolute Error : The mean absloute error for the Stock Price prediction is 169.99 while the mean absloute error for stock returns is 0.91

Based on the RMSE and mean absolute error, we can say that the model predicts stock returns more accurately than it predicts the stock prices, hence reinforcing the fact that it is difficult to predict stock prices.

## HEAD
- What is the future value of the customers' stocks based on their current portafolio? (prediction)


3b59eca2d3d62adc964daee083f2232ef4ffb1ee
