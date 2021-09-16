# climate-sensitive-diseases

A collection of analyses and prediction models for two climate sensitive diseases in Vietnam — dengue fever (DF) and diarrhoea.

## Overview:
 - Traditional machine learning and deep learning models for disease forecasting
 - Boxplots, barplots, and geospatial maps to visualise the relationships between climate factors, regions, and disease rates
 - Tree-structured Parzen Estimator (TPE) hyperparameter optimisation implemented through [Optuna](https://github.com/optuna/optuna)
 - Summary statistics, Kruskal-wallis tests, and posthoc Dunn's tests used to investigate differences in climate between regions
 - [Data availability statement](#data-availability-statement)


| Folder                     | File                          | Description                                                        |
| -------------------------- | ----------------------------- | ------------------------------------------------------------------ |
| **figures**                | `[All]`                       | Examples figures                                                   |
| **data**                   | `population_data.xlsx`        | Populations per province from 1997–2016                            |
| **data**                   | `vietnam.json`                | Vietnam province shapes for geospatial mapping                     |
| **data_processing**        | `calculate_rates.py`          | Calculate disease incidence rates                                  |
| **data_processing**        | `data_stats.py`               | Summary stats and statistical tests                                |
| **data_processing**        | `data_test_stationary.py`     | Dickey-fuller test, decomposition, ACF/PACF                        |
| **optimisation**           | `optuna_cnn.ipynb`            | TPE optimisation of CNNs                                           |
| **optimisation**           | `optuna_lstm.ipynb`           | TPE optimisation of LSTM and LSTM-ATT models                       |
| **optimisation**           | `optuna_sarima.py`            | TPE optimisation of SARIMA models                                  | 
| **optimisation**           | `optuna_thai_jobscript.sh`    | SLURM HPC jobscript for optuna_sarima.py                           |
| **optimisation**           | `sarima_grid_kelvin.py`       | SARIMA hyperparameter grid search                                  |
| **optimisation**           | `thai_binh_jobscript.sh`      | SLURM HPC jobscript for sarima_grid_kelvin.py                      |
| **optimisation**           | `optuna_thai_jobscript.sh`    | SLURM HPC jobscript for optuna_sarima.py                           |
| **plotting**               | `diarrhoea_plots.py`          | Boxplots and heatmaps of diarrhoea/DF rates & climate-correlations |
| **plotting**               | `lstm-att_outbreaks.ipynb`    | Plots figures for outbreak detection metrics                       |
| **plotting**               | `mapping.py`                  | Creates GeoPandas geospatial maps of disease rates                 |
| **plotting**               | `multi_month_plot.ipynb`      | Plots multi-month predictions                                      |
| **prediction_models**      | `pytorch_dengue_fever.ipynb`  | Pytorch LSTM, LSTM-ATT, and CNN models for DF predictions          |
| **prediction_models**      | `pytorch_diarrhoea.ipynb`     | Pytorch LSTM, LSTM-ATT, and CNN models for diarrhoea predictions   |
| **prediction_models**      | `sarima(x).ipynb`             | SARIMA and SARIMAX models for disease forecasting                  |






 - Data is private
 - Pytorch code is currently private
 - OPTUNA hyperparameter optimisation for Pytorch models is currently private
 - **mapping.py** creates a GeoPandas geospatial map of diarrhoea rates
 - **diarrhoea_plots.py** creates boxplots and heatmaps of diarrhoea rates and correlations with climate factors
 - **sarima_grid_kelvin.py** is a hyperparameter gridsearch for a SARIMA diarrhoea prediction model (must be run on HPC cluster)
 - **thai_binh_sarima_best.py** is for diarrhoea prediction in the Thai Binh province using hyperparameters obtained from the gridsearch
 - **thai_binh_multi_sarimax.py** is a multivariate version of the SARIMA model
 - **thai_binh_jobscript.sh** schedules and allocates resources for the SARIMA gridsearch as a SLURM HPC job
 - **optuna_thai_jobscript.sh** schedules and allocates resources for the OPTUNA hyperparameter optimisation as a SLURM HPC job
<br />

## Diarrhoea rates by province
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/diarrhoea_rates_by_province.png?raw=true)
<br />

## Geospatial map of diarrhoea rates per 100k population
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/diarrhoea_rates_map.png?raw=true)
<br />

## LSTM-Attention prediction of diarrhoea rates in Thai Binh
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/thai_binh_lstm_att.png?raw=true)
 - MAPE: 3.65%
 - RMSE: 16.78
<br />

## SARIMA prediction of diarrhoea rates in Thai Binh (including training data)
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/thai_binh_SARIMA.png?raw=true)
 - MAPE: 11.16%
 - RMSE: 53.13
<br />

## SARIMAX prediction of diarrhoea rates in Thai Binh (including training data)
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/thai_binh_multi_SARIMAX.png?raw=true)
 - MAPE: 9.71%

## Data Availability Statement

