# climate-sensitive-diseases

A collection of analyses and prediction models for climate sensitive diseases in Vietnam. This repo is a public version of a larger private repo, as there are restrictions in place for the private data being used.

## Overview:
 - Data is private
 - Pytorch code is currently private
 - OPTUNA hyperparameter optimisation for Pytorch models is currently private
 - **mapping.py** creates GeoPandas geospatial map of diarrhoea cases in Vietnam
 - **diarrhoea_plots.py** creates boxplots and heatmaps of diarrhoea rates and correlations with climate factors in Vietnam
 - **sarima-grid-kelvin.py** is a hyperparameter gridsearch for a SARIMA diarrhoea prediction model (must be run on HPC cluster)
 - **thai-binh-sarima-best.py** is for diarrhoea prediction in the Thai Binh province from the gridsearch results
 - **thai-binh-multi-sarimax.py** is a multivariate version of the SARIMA model
 - **thai_binh_jobscript.sh** schedules and allocates resources for the SARIMA gridsearch as a SLURM HPC job
 - **optuna_thai_jobscript** schedules and allocates resources for the OPTUNA hyperparameter optimisation as a SLURM HPC job

## Diarrhoea rates by province:
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/diarrhoea_rates_by_province.png?raw=true)

## Geospatial map of diarrhoea rates per 100k population:
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/diarrhoea_rates_map.png?raw=true)

## SARIMA prediction
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/thai_binh_SARIMA.png?raw=true)

## SARIMAX prediction
![alt text](https://github.com/mullach/climate-sensitive-diseases/blob/main/Figures/thai_binh_multi_SARIMAX.png?raw=true)
