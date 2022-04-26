#!/bin/bash -l
#SBATCH --ntasks 1 # The number of cores you need...
#SBATCH --array=1-12%12
#SBATCH -p cosma6 #or some other partition, e.g. cosma, cosma6, etc.
#SBATCH -A dp004
#SBATCH --cpus-per-task=1
#SBATCH -J FLARES_SFH_fitting #Give it something meaningful.
#SBATCH -o logs/output_hlr_job.%A_%a.out
#SBATCH -e logs/error_hlr_job.%A_%a.err
#SBATCH -t 24:00:00

# Run the job from the following directory - change this to point to your own personal space on /lustre
cd /cosma/home/dp004/dc-wilk2/data/flare/projects/flares_sfzh/analysis/sfh/


module purge
#load the modules used to build your program.
module load python/3.9.1-C7 gnu_comp/11.1.0 openmpi/4.1.1 ucx/1.10.1

source /cosma/home/dp004/dc-wilk2/python_venv/bin/activate

i=$(($SLURM_ARRAY_TASK_ID - 1))

# Run the program
srun python3 measure_distribution_parameters.py $i halfnorm
srun python3 measure_distribution_parameters.py $i truncnorm
srun python3 measure_distribution_parameters.py $i trunclognorm

echo "Job done, info follows..."
sacct -j $SLURM_JOBID --format=JobID,JobName,Partition,MaxRSS,Elapsed,ExitCode
exit
