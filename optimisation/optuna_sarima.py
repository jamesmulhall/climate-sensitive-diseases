# grid search sarima hyperparameters
from math import sqrt
from warnings import catch_warnings
from warnings import filterwarnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
import pandas as pd
import optuna


# one-step sarima forecast
def sarima_forecast(history, config):
    """Forecasts 1-month ahead"""
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
    """Returns RMSE"""
    return sqrt(mean_squared_error(actual, predicted))


# split a univariate dataset into train/test sets
def train_test_split(data, n_test):
    """Returns train and test sets"""
    return data[:-n_test], data[-n_test:]


# walk-forward validation for univariate data
def walk_forward_validation(data, n_test, cfg):
    """Returns RMSE on walk forward validation"""
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
    """
    Runs walk_forward_validation function on cfg, a set
    of model parameters
    """
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

def objective(trial):
    """
    Optuna runs this function to find which combination of parameters
    will result in the lowest RMSE
    """
    # Let Optuna suggest parameters
    p = trial.suggest_int('p', 1, 6)
    d = trial.suggest_int('d', 0, 1)
    q = trial.suggest_int('q', 1, 6)
    t = trial.suggest_categorical('t', ['n', 'c', 't', 'ct'])
    P = trial.suggest_int('P', 0, 6)
    D = trial.suggest_int('D', 0, 1)
    Q = trial.suggest_int('Q', 0, 6)
    m = trial.suggest_categorical('m', [6, 12])

    # Combination of parameters to be tested
    cfg = [(p, d, q), (P, D, Q, m), t]

    # data split
    n_test = 1

    # score
    _, result = score_model(data, n_test, cfg)

    return result


if __name__ == '__main__':
    # load dataset
    vietnam = pd.read_excel("/mnt/scratch2/users/40296869/100k_anglicised.xlsx", engine = 'openpyxl')
    vietnam = vietnam.loc[vietnam['year_month'] < '2014-1-1']
    dfbase = vietnam.loc[vietnam['province'] == "Thái Bình"]
    
    # create data to fit
    df = dfbase[['Diarrhoea_rates']]
    ddatefull = [pd.Timestamp(x) for x in list(dfbase.year_month)]

    df['Date'] = ddatefull
    df = df.set_index("Date")
    print("Data \n", df)

    # data
    data = df['Diarrhoea_rates']

    # Use Tree-structured Parzen Estimator sampler to optimise
    sampler = optuna.samplers.TPESampler()
    study = optuna.create_study(sampler=sampler, direction='minimize')

    # Optimise over 100 trials
    study.optimize(objective, n_trials=100, n_jobs=-1)

    # Print results
    print("Study statistics for : ")
    print("  Number of finished trials: ", len(study.trials))
    print("  Number of pruned trials: ", len(pruned_trials))
    print("  Number of complete trials: ", len(complete_trials))
    
    print("Best trial:")
    trial = study.best_trial
    print("  Value: ", trial.value)
    print("  Params: ")
    for key, value in trial.params.items():
        print("    {}: {}".format(key, value))