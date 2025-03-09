#!/bin/bash
###############################################################################
## SLURM Options
#SBATCH --time=04:00:00                  # Job run time (hh:mm:ss)
#SBATCH --nodes=1                        # Number of nodes
#SBATCH --ntasks-per-node=2             # Number of task (cores/ppn) per node
#SBATCH --cpus-per-task=4 
#SBATCH --mem=64GB
#SBATCH --job-name=metrics  # Job name
#SBATCH --partition=eng-instruction      # Partition (queue)
#SBATCH --account=25sp-cs598gck-eng      # Batch account to use
#SBATCH --output=metrics.o%j  # Name of batch job output i

python test_modularity_2.py
