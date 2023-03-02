# LSTM Time Series Prediction
This repository contains a Jupyter notebook DMAML_CW2_PartB_Shams.ipynb that demonstrates how to use LSTM to predict stock prices using time series data.

### Libraries Used
- numpy
- matplotlib
- pandas
- seaborn
- sklearn
- keras
- pandas_profiling
### Dataset
The dataset used for this project is the stock prices of Netflix, obtained from Yahoo Finance. The data covers the time period from May 24, 2002, to April 17, 2022.

### Installation
To run the notebook, the necessary libraries must be installed. You can do this by running the following command in the notebook:
! pip install https://github.com/pandas-profiling/pandas-profiling/archive/master.zip

### How to Use
The notebook explains the process step-by-step and includes detailed explanations of the code used.

1. Import the necessary libraries
2. Read the data using pandas
3. Understand the data by checking its properties
4. Normalize the dataset
5. Split the data into training and testing sets
6. Reshape the data for the LSTM model
7. Create and fit the LSTM network
8. Make predictions
9. Invert the predictions to get actual values
10. Calculate root mean squared error
11. Plot the predictions
