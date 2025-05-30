#!/bin/bash

#SBATCH -J inf_gan_test
#SBATCH -o run_logs/job.o%j
#SBATCH -e run_logs/job.e%j
#SBATCH -p gpu-a100-small
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 05:00:00
#SBATCH --mail-type=all
#SBATCH --mail-user=briankim31415@gmail.com
#SBATCH -A ASC24027

module load gcc cuda python3
source ./inf_gan/bin/activate
python3 examples/sde_gan.py