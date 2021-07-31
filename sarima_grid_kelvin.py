# grid search sarima hyperparameters
from math import sqrt
from multiprocessing import cpu_count
from joblib import Parallel
from joblib import delayed
from warnings import catch_warnings
from warnings import filterwarnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from pandas import read_csv
import pandas as pd
import numpy as np

# one-step sarima forecast
def sarima_forecast(history, config):
    order, sorder, trend = config
    # define model
    model = SARIMAX(history, order=order, seasonal_order=sorder, trend=trend, enforce_stationarity=False,
                    enforce_invertibility=False)
    # fit model
    model_fit = model.fit(disp=False)
    # make one step forecast
    yhat = model_fit.predict(len(history), len(history))
    return yhat[0]

# root mean squared error or rmse
def measure_rmse(actual, predicted):
    return sqrt(mean_squared_error(actual, predicted))


# split a univariate dataset into train/test sets
def train_test_split(data, n_test):
    return data[:-n_test], data[-n_test:]


# walk-forward validation for univariate data
def walk_forward_validation(data, n_test, cfg):
    predictions = list()
    # split dataset
    train, test = train_test_split(data, n_test)
    # seed history with training dataset
    history = [x for x in train]
    # step over each time-step in the test set
    for i in range(len(test)):
        # fit model and make forecast for history
        yhat = sarima_forecast(history, cfg)
        # store forecast in list of predictions
        predictions.append(yhat)
        # add actual observation to history for the next loop
        history.append(test[i])
    # estimate prediction error
    error = measure_rmse(test, predictions)
    return error


# score a model, return None on failure
def score_model(data, n_test, cfg, debug=False):
    result = None
    # convert config to a key
    key = str(cfg)
    # show all warnings and fail on exception if debugging
    if debug:
        result = walk_forward_validation(data, n_test, cfg)
    else:
        # one failure during model validation suggests an unstable config
        try:
            # never show warnings when grid searching, too noisy
            with catch_warnings():
                filterwarnings("ignore")
                result = walk_forward_validation(data, n_test, cfg)
        except:
            error = None
    # check for an interesting result
    if result is not None:
        print(' > Model[%s] %.3f' % (key, result))
    return (key, result)


# grid search configs
def grid_search(data, cfg_list, n_test, parallel=True):
    scores = None
    if parallel:
        # execute configs in parallel -- changed from cpu_count() to 64 for HPC use
        executor = Parallel(n_jobs=64, backend='multiprocessing')
        tasks = (delayed(score_model)(data, n_test, cfg) for cfg in cfg_list)
        scores = executor(tasks)
    else:
        scores = [score_model(data, n_test, cfg) for cfg in cfg_list]
    # remove empty results
    scores = [r for r in scores if r[1] != None]
    # sort configs by error, asc
    scores.sort(key=lambda tup: tup[1])
    return scores


# create a set of sarima configs to try
def sarima_configs(seasonal=[0]):
    models = list()
    # define config lists
    p_params = [0, 1, 2, 3, 4, 5, 6]
    d_params = [0, 1]
    q_params = [0, 1, 2, 3, 4]
    t_params = ['n', 'c', 't', 'ct']
    P_params = [0, 1, 2, 3, 4, 5, 6]
    D_params = [0, 1]
    Q_params = [0, 1, 2, 3, 4]
    m_params = seasonal
    # create config instances
    for p in p_params:
        for d in d_params:
            for q in q_params:
                for t in t_params:
                    for P in P_params:
                        for D in D_params:
                            for Q in Q_params:
                                for m in m_params:
                                    cfg = [(p, d, q), (P, D, Q, m), t]
                                    models.append(cfg)
    return models


if __name__ == '__main__':
    # load dataset
    vietnam = pd.read_excel("/mnt/scratch2/users/40296869/100k_anglicised.xlsx", engine = 'openpyxl')
    vietnam = vietnam.loc[vietnam['year_month'] < '2014-1-1']
    dfbase = vietnam.loc[vietnam['province'] == "Thái Bình"]

    # create data to fit
    df = dfbase[['Diarrhoea_rates']]
    ddatefull = [pd.Timestamp(x) for x in list(dfbase.year_month)]

    # print(ddatefull)
    df['Date'] = ddatefull
    df = df.set_index("Date")
    print("Data \n", df)

    # data
    data = df['Diarrhoea_rates']

    # data split
    n_test = 1
    # model configs
    cfg_list = sarima_configs(seasonal=[0, 12])
    # grid search
    scores = grid_search(data, cfg_list, n_test)
    # done
    print('done')
    # list top 3 configs
    for cfg, error in scores[:10]:
        print(cfg, error)
        f = open("sarima_thai_binh.txt", "a")
        print(cfg, error, file = f)
        f.close()