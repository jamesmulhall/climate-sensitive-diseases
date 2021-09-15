#!/bin/bash
#SBATCH --job-name=SARIMA_thai_binh
#SBATCH --output=/mnt/scratch2/users/40296869/thai_binh_results.out
#SBATCH --mail-user=jmulhall03@qub.ac.uk
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

#SBATCH --ntasks=64
#SBATCH --nodes=1

#SBATCH --mem-per-cpu=2G

#SBATCH --time=0-23:59:00
#SBATCH --partition=k2-medpri

module load apps/anaconda3/5.2.0/bin
source activate my-env

echo "Starting SARIMA grid search"
python3 /mnt/scratch2/users/40296869/sarima_grid_kelvin.py
echo "Finished SARIMA"

conda deactivate