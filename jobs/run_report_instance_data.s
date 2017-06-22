#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=20:00:00
#SBATCH --mem=10GB
#SBATCH --job-name=report_instance_data1
#SBATCH --mail-type=END
#SBATCH --mail-user=zb9@nyu.edu
#SBATCH --output=report_ins_data1_%j.out

run_id=${SLURM_ARRAY_TASK_ID}
module purge
module load python/intel/2.7.12


cd /scratch/$USER/rushhour/src
python run_report_instance_data.py 1 ${run_id} >> ../output/report_LRTA_instance_data${run_id}.txt
