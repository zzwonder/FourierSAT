#!/bin/bash
mkdir results_2024

./run.slurm randomInstances/cards fouriersat unconstrained_SQUARE_HJ 1 square HJPROX_PARALLEL 0 0.8 solver

