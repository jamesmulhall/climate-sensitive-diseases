### Package usage
import warnings
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot
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

import matplotlib
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'
import seaborn as sns

class Opt:
    show = True

### Load the data
vietnam = pd.read_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\climate-sensitive-diseases-private\\full_data_fixed.xlsx")
dfbase = vietnam.loc[vietnam['province'] == "Điện Biên"]
#dfbase = pd.read_csv("Binh_050_full.csv", parse_dates=True)
#dfbase = pd.read_csv("test.csv", parse_dates=True)

### Create data to fit
df = dfbase[['Diarrhoea_rates']]
ddatefull = [pd.Timestamp(x) for x in list(dfbase.year_month)]
#print(ddatefull)
df['Date'] = ddatefull
df = df.set_index("Date")

def impute_missing_value(city_data):
    """
    Imputes 0 for first 12 months, 
    last year's value for months 12-24, 
    and minimum value of last two years for months 25+
    """
    for col in city_data.columns:
        for index in range(len(city_data[col])):
            if np.isnan(city_data[col].iloc[index]):
                if index < 12:
                    city_data[col].iloc[index] = 0
                elif index >= 12 and index <= 24:
                    city_data[col].iloc[index] = city_data[col].iloc[index - 12]
                else:
                    city_data[col].iloc[index] = min(city_data[col].iloc[index - 12], city_data[col].iloc[index - 24])
    return city_data

df = impute_missing_value(df)

# 1 Diff
df["Diarrhoea_rates"] = df["Diarrhoea_rates"] - df["Diarrhoea_rates"].shift()
df = df[1:]
print(df)

### Plot the data
df.plot(figsize=(15,6))
plt.show()

# Reviewing plots of the density of observations can provide further insight into the structure of the data
pyplot.figure(1)
pyplot.subplot(211)
df.Diarrhoea_rates.hist()
pyplot.subplot(212)
df.Diarrhoea_rates.plot(kind = 'kde')
pyplot.show()

# Box and Whisker Plots
fig, ax = plt.subplots(figsize = (15, 6))
sns.boxplot(df.Diarrhoea_rates.index.year, df.Diarrhoea_rates, ax = ax)

# Decomposing using statsmodel
from pylab import rcParams

def decomposing(timeseries):
    rcParams['figure.figsize'] = 16, 6
    decomposition = sm.tsa.seasonal_decompose(timeseries, model='additive')
    fig = decomposition.plot()
    plt.show()

decomposing(df)

# ACF and PACF plots
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf

def acf_and_pacf_plot(ts, lag = 30):
    pyplot.figure()
    pyplot.subplot(211)
    plot_acf(ts, ax=pyplot.gca(), lags = lag)
    pyplot.subplot(212)
    plot_pacf(ts, ax=pyplot.gca(), lags = lag)
    pyplot.show()

acf_and_pacf_plot(df.Diarrhoea_rates, 30)

# Test stationarity
def test_stationarity(timeseries):

    #Determing rolling statistics
    rolmean = timeseries.rolling(12).mean()
    rolstd = timeseries.rolling(12).std()

    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

    # Perform Dickey-Fuller test
    print ('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)

test_stationarity(df)

# Making timeseries stationary
ts_log = np.log(df)
ts_log_diff = ts_log.Diarrhoea_rates - ts_log.Diarrhoea_rates.shift()
ts_log_diff.dropna(inplace=True)

test_stationarity(ts_log_diff)

