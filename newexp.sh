#!/bin/bash
mkdir results_2024

./run.slurm randomInstances/CNF_1000 fouriersat unconstrained_SQUARE_HJ 1 square HJPROX_PARALLEL 0 0 dev 
./run.slurm randomInstances/XOR_1000 fouriersat unconstrained_SQUARE_HJ 1 square HJPROX_PARALLEL 0 0 dev
./run.slurm randomInstances/cnfxor fouriersat unconstrained_SQUARE_HJ 1 square HJPROX_PARALLEL 0 0 solver

./run.slurm randomInstances/CNF_1000 fouriersat unconstrained_ABS_HJ 1 abs HJPROX_PARALLEL 0 0 dev 
./run.slurm randomInstances/XOR_1000 fouriersat unconstrained_ABS_HJ 1 abs HJPROX_PARALLEL 0 0 dev
./run.slurm randomInstances/cnfxor fouriersat unconstrained_ABS_HJ 1 abs HJPROX_PARALLEL 0 0 solver

