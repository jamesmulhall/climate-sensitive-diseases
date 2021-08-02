# climate-sensitive-diseases

A collection of analyses and prediction models for climate sensitive diseases in Vietnam. This repo is a public version of a larger private repo, as there are restrictions in place for the private data being used.

## Overview:
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
