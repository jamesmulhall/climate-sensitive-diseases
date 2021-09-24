import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn import linear_model
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, median_absolute_error, mean_squared_log_error
from itertools import combinations
import os
import csv
from sklearn import preprocessing
from xgboost import XGBRegressor
from sklearn.svm import SVR

methodname = "poisson"

# dataname
provinces = [
    "Hà Nội",
    'Hải Phòng',
    'Quảng Ninh',
    'Nam Định',
    'Thái Bình',
    'Quảng Nam',
    'Quảng Ngãi',
    'Phú Yên',
    'Ninh Thuận',
    'Bình Thuận',
    'Tây Ninh',
    'Bình Phước',
    'An Giang',
    'Tiền Giang',
    'Cần Thơ',
    'Trà Vinh',
    'Kiên Giang',
    'Sóc Trăng',
    'Bạc Liêu',
    'Cà Mau'
]

def evaluate_forecast(y, pred):
    results = pd.DataFrame({'r2_score':r2_score(y, pred),
                           }, index=[0])
    results['mae'] = mean_absolute_error(y, pred)
    results['mse'] = mean_squared_error(y, pred)
    results['rmse'] = np.sqrt(results['mse'])
    return results


proerrs = {}

for dataname in provinces:
    print("******************************************************************")
    print("PROVINCE : ", dataname)

    # read the data
    data = pd.read_excel(dataname + ".xlsx", engine='openpyxl')
    data = data.fillna(0)
    data = data.replace(np.nan, 0)
    print(data.head())

    # split into training and testing set
    sizetrain = 204
    sizetest = 36

    xlist = ['year_month', 'Total_Evaporation',	'Total_Rainfall',	'Max_Daily_Rainfall',	'n_raining_days',
             'Average_temperature',	'Max_Average_Temperature',	'Min_Average_Temperature',	'Max_Asolute_Temperature',
             'Min_Asolute_Temperature',	'Average_Humidity',	'Min_Humudity',	'n_hours_sunshine']
    #xlist = ['year_month', 'Total_Evaporation',	'Total_Rainfall']

    ylist = ['year_month', 'Dengue_fever_rates']

    datatrain = data.loc[0:203]
    print("Train = ", datatrain)
    datatrainy = datatrain[ylist]
    datatrainy = datatrainy.set_index('year_month')
    datatest = data.loc[204:]
    print("Test = ", datatest)
    datatesty = datatest[ylist]
    datatesty = datatesty.set_index('year_month')

    yscaler = preprocessing.MinMaxScaler()
    datatrainy = yscaler.fit_transform(datatrainy)
    datatesty = yscaler.transform(datatesty)

    combs = list(combinations(xlist[1:], 2)) + list(combinations(xlist[1:], 3)) + list(combinations(xlist[1:], 4)) \
            +  list(combinations(xlist[1:], 5)) +  list(combinations(xlist[1:], 6))  + list(combinations(xlist[1:], 7))

    print("Number of combinations = ", len(combs))
    #print(combs)

    bestmae = 100000000
    bestpredict = None
    bestclimate = None

    for item in combs:

        print("Climate factors : ", item)
        climatefactors = ['year_month'] + [x for x in item]

        datatrainx = datatrain[climatefactors]
        datatrainx = datatrainx.set_index('year_month')
        datatestx = datatest[climatefactors]
        datatestx = datatestx.set_index('year_month')

        xscaler = preprocessing.MinMaxScaler()
        datatrainx = xscaler.fit_transform(datatrainx)
        datatestx = xscaler.transform(datatestx)

        # poisson regression
        clf = linear_model.PoissonRegressor(alpha=1e-15, max_iter=1000000)
        #print(datatrainy.values.ravel())
        clf.fit(datatrainx, datatrainy.ravel())

        yh = clf.predict(datatestx)
        print("Yh = ", yh)

        results = {}
        results['Real'] = datatest['Dengue_fever_rates'].values.ravel()
        results['Predict'] = (yscaler.inverse_transform(yh.reshape(-1, 1))).ravel()

        for i in range(len(results['Predict'])):
            if results['Predict'][i] < 0:
                results['Predict'][i] = 0

        errs = evaluate_forecast(results['Real'], results['Predict'])
        print(errs)

        if errs['mae'][0] < bestmae:
            bestmae = errs['mae'][0]
            bestpredict = results
            bestclimate = climatefactors

    print("Best results = ", bestpredict)
    print("Best MAE = ", bestmae)
    print("Best climates = ", bestclimate)
    errs = evaluate_forecast(bestpredict['Real'], bestpredict['Predict'])
    print(errs)

    proerrs[dataname] = [errs['rmse'][0], errs['mae'][0]]

    # save to file
    df = pd.DataFrame()
    for c in bestclimate:
        df[c] = datatest[c]
    df['Real'] = bestpredict['Real']
    df['Predict'] = bestpredict['Predict']

    df.to_csv("out_" + dataname + "_" + methodname + ".csv")

# Save to file
lst = []
for dataname in provinces:
    lst.append(proerrs[dataname])

with open("out_" + methodname + ".csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(lst)



