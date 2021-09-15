#!/bin/bash
#SBATCH --job-name=OPTUNA_thai_binh
#SBATCH --output=/mnt/scratch2/users/40296869/OPTUNA_thai_binh.out
#SBATCH --mail-user=jmulhall03@qub.ac.uk
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

#SBATCH --time=0-0:60:00
#SBATCH --partition=k2-gpu

#SBATCH --mem-per-cpu=16G

module load apps/anaconda3/5.2.0/bin
module load libs/nvidia-cuda/11.0.3/bin

source activate my-env

echo "Starting OPTUNA search"
python3 /mnt/scratch2/users/40296869/optuna_diarrhoea_prediction.py
echo "Finished OPTUNA search"

conda deactivate