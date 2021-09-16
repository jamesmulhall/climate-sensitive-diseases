# climate-sensitive-diseases

A collection of analyses and prediction models for two climate sensitive diseases in Vietnam — dengue fever (DF) and diarrhoea.
<br />
<br />

## Overview:
 - Traditional machine learning and deep learning models for disease forecasting
 - Boxplots, barplots, and geospatial maps to visualise the relationships between climate factors, regions, and disease rates
 - Tree-structured Parzen Estimator (TPE) hyperparameter optimisation implemented through [Optuna](https://github.com/optuna/optuna)
 - Summary statistics, Kruskal-wallis tests, and post hoc Dunn's tests used to investigate differences in climate between regions
 - Google Colab is required for the Google Drive integration in .ipynb files
 - [Data availability statement](#data-availability-statement)
<br />

## Description of files
| Folder                     | File                          | Description                                                        |
| :------------------------- | :---------------------------- | :----------------------------------------------------------------- |
| **figures**                | `[All]`                       | Example figures                                                    |
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
| **plotting**               | `disease_plots.py`            | Boxplots and heatmaps of diarrhoea/DF rates & climate-correlations |
| **plotting**               | `lstm-att_outbreaks.ipynb`    | Plots figures for outbreak detection metrics                       |
| **plotting**               | `mapping.py`                  | Creates GeoPandas geospatial maps of disease rates                 |
| **plotting**               | `multi_month_plot.ipynb`      | Plots multi-month predictions                                      |
| **prediction_models**      | `pytorch_dengue_fever.ipynb`  | Pytorch LSTM, LSTM-ATT, and CNN models for DF predictions          |
| **prediction_models**      | `pytorch_diarrhoea.ipynb`     | Pytorch LSTM, LSTM-ATT, and CNN models for diarrhoea predictions   |
| **prediction_models**      | `sarima(x).ipynb`             | SARIMA and SARIMAX models for disease forecasting                  |
<br />

## Dengue Fever rates by province
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/df_rates_by_province.png?raw=true)
<br />
<br />

## Diarrhoea rates by province
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/diarrhoea_rates_by_province.png?raw=true)
<br />
<br />

## Geospatial map of disease rates per 100k population
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/disease_maps.svg?raw=true)
<br />
<br />

## SARIMA(X) diarrhoea predictions
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/sarimax_diarrhoea_pred.png?raw=true)
<br />
<br />

## Deep learning diarrhoea predictions
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/pytorch_diarrhoea_pred.png?raw=true)
<br />
<br />

## LSTM-ATT multi-month ahead predictions for diarrhoea
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/multi-month_lstm-att.png?raw=true)
<br />
<br />

## Data Availability Statement
The population data used to calculate disease incidence rates per province per year are publicly available from the General Statistics Office of Vietnam [here](https://www.gso.gov.vn/en/population/). The climate and disease data were obtained for a fee from the Vietnam Institute of Meteorology, Hydrology and Climate Change (IMHEN) and the Vietnam National Institute of Hygiene and Epidemiology (NIHE), respectively. Restrictions apply to the availability of the data, which is available from the author with the permission of the respective institutions. Alternatively, data can be requested directly from IMHEN and NIHE.
