#!/bin/bash -login
#PBS -N Job_Name
#PBS -l nodes=2:ppn=8
#PBS -l walltime=03:55:00
#PBS -l mem=32gb
#PBS -k oe
#PBS -j oe

source activate

cd ${PBS_O_WORKDIR}

mpirun -np 16 python file_name.py

exit 0
