#!/bin/bash
mkdir results_2024
for beta10 in $(seq 0 2 9);
do
          ./run.slurm randomInstances/cards fouriersat unconstrained_SQUARE_HJ_1.$beta10 1 square HJPROX 0 1.$beta10 solver
          ./run.slurm randomInstances/cards fouriersat unconstrained_SQUARE_HJ_0.$beta10 1 square HJPROX 0 0.$beta10 solver
          ./run.slurm randomInstances/CNF_1000 fouriersat unconstrained_SQUARE_HJ_0.$beta10 1 square HJPROX 0 0.$beta10 dev 
          ./run.slurm randomInstances/XOR_1000 fouriersat unconstrained_SQUARE_HJ_0.$beta10 1 square HJPROX 0 0.$beta10 dev
          ./run.slurm randomInstances/cards fouriersat unconstrained_ABS_HJ_1.$beta10 1 abs HJPROX 0 1.$beta10 solver
          ./run.slurm randomInstances/cards fouriersat unconstrained_ABS_HJ_0.$beta10 1 abs HJPROX 0 0.$beta10 solver
          ./run.slurm randomInstances/CNF_1000 fouriersat unconstrained_ABS_HJ_0.$beta10 1 abs HJPROX 0 0.$beta10 dev
          ./run.slurm randomInstances/XOR_1000 fouriersat unconstrained_ABS_HJ_0.$beta10 1 abs HJPROX 0 0.$beta10 dev
done     

