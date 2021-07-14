### Package usage
import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')

import pandas as pd
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARMA, ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

from math import sqrt

import matplotlib
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'
import seaborn as sns

from random import random

from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, median_absolute_error, mean_squared_log_error
from pandas import DataFrame
from matplotlib import pyplot

# evaluate model
def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def evaluate_forecast(y, pred):
    results = pd.DataFrame({'r2_score':r2_score(y, pred),
                           }, index=[0])
    results['mean_absolute_error'] = mean_absolute_error(y, pred)
    results['median_absolute_error'] = median_absolute_error(y, pred)
    results['mse'] = mean_squared_error(y, pred)
    results['msle'] = mean_squared_log_error(y, pred)
    results['mape'] = (mean_absolute_percentage_error(y, pred)).values
    results['rmse'] = np.sqrt(results['mse'])
    return results

### Load the data
#dfbase = pd.read_csv("Binh_050_full.csv", parse_dates=True)
vietnam = pd.read_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\100k_anglicised.xlsx")
vietnam = vietnam.loc[vietnam['year_month'] < '2014-1-1']
dfbase = vietnam.loc[vietnam['province'] == "Thái Bình"]

### Create data to fit
df = dfbase[['Diarrhoea_rates']]
ddatefull = [pd.Timestamp(x) for x in list(dfbase.year_month)]
#print(ddatefull)
df['Date'] = ddatefull
df = df.set_index("Date")
print("Data \n", df)

# number of sample
numdata = len(df)

# number of test
#numtest = 182
# last 3 years 2014-2016
numtest = 36

# divide into train and validation set
train = df[:(numdata - numtest)]
test = df[(numdata - numtest):]

print("TRAIN", train)
print("TEST", test)

start_index = test.index.min()
end_index = test.index.max()
start_pos = numdata - numtest
end_pos = numdata

print("Start index: ", start_index, " End index: ", end_index)
print("Start position: ", start_pos, " End position: ", end_pos)

# train and prediction
predictions = list()

trainlist = [x for x in train.Diarrhoea_rates]
testlist = [x for x in test.Diarrhoea_rates]

print("TrainList : ", trainlist)
print("TestList : ", testlist)

# prediction step
nstep = 1

# retrain the model
retrain = True

# set the model config
order = (0, 0, 1)
sorder = (6, 0, 3, 12)
trend = 'n'

# a first model to look at
model = SARIMAX(trainlist, order=order, seasonal_order=sorder, trend=trend,
                    enforce_stationarity=False,
                    enforce_invertibility=False)
# fit model
model_fit = model.fit(disp=False)
print(model_fit.summary())

# line plot of residuals
residuals = DataFrame(model_fit.resid)
residuals.plot()
pyplot.show()

# density plot of residuals
residuals.plot(kind='kde')
pyplot.show()

# summary stats of residuals
print(residuals.describe())

# step over each time-step in the test set
for i in range(len(testlist) - nstep + 1):
    print("Iteration ", i)
    if retrain:
        # define model
        model = SARIMAX(trainlist, order=order, seasonal_order=sorder, trend=trend,
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        # fit model
        model_fit = model.fit(disp=False)
        print(model_fit.summary())
    # forecast
    yhat = model_fit.predict(len(trainlist), len(trainlist) + nstep - 1)
    # print the prediction
    print("Prediction   : ", yhat)
    print("Real         : ", testlist[i : i + nstep])
    # take the prediction result
    predictions.append(yhat[nstep - 1])
    # add actual observation to history for the next loop
    trainlist.append(testlist[i])

# print final model
print("Final model: ")
print(model_fit.summary())

# print out the prediction
print("TrainList : ", trainlist)
print("TestList : ", testlist)
print("Prediction: ", predictions)

# prediction
predorg = df[(numdata - numtest + nstep - 1):].copy()
pred = df[(numdata - numtest + nstep - 1):].copy()
pred['Diarrhoea_rates'] = predictions

# plot the data
train['Diarrhoea_rates'].plot()
test['Diarrhoea_rates'].plot()
pred['Diarrhoea_rates'].plot()
plt.show()

# evaluate forecast
print(f"Predorg: {predorg}")
print(f"Pred: {pred}")
results = evaluate_forecast(predorg, pred)
print(results)

print("End prediction")

