#!/bin/bash
#sbatch run.slurm randomInstances/CNF_1000 fouriersat constrained_SQUARE_SLSQP 0 square SLSQP
#sbatch run.slurm randomInstances/CNF_1000 fouriersat constrained_ABS_SLSQP 0 abs SLSQP   
#sbatch run.slurm randomInstances/CNF_1000 fouriersat constrained_SQUARE_GD 0 square GD
#sbatch run.slurm randomInstances/CNF_1000 fouriersat constrained_ABS_GD 0 abs GD
#sbatch run.slurm randomInstances/CNF_1000 fouriersat unconstrained_ABS_SLSQP 1 abs SLSQP
#sbatch run.slurm randomInstances/XOR_1000 fouriersat constrained_SQUARE_SLSQP 0 square SLSQP
#sbatch run.slurm randomInstances/XOR_1000 fouriersat constrained_ABS_SLSQP 0 abs SLSQP
#sbatch run.slurm randomInstances/XOR_1000 fouriersat constrained_SQUARE_GD 0 square GD
#sbatch run.slurm randomInstances/XOR_1000 fouriersat constrained_ABS_GD 0 abs GD
#sbatch run.slurm randomInstances/XOR_1000 fouriersat unconstrained_ABS_SLSQP 1 abs SLSQP
"""
sbatch run.slurm  benchmarks/MAXSAT_benchmarks/ fouriersat constrained_SQUARE_SLSQP 0 square SLSQP 1
sbatch run.slurm  benchmarks/MAXSAT_benchmarks/ fouriersat unconstrained_SQUARE_SLSQP 1 square SLSQP 1

sbatch run.slurm  benchmarks/MAXSAT_benchmarks/ fouriersat constrained_ABS_SLSQP 0 abs SLSQP 1
sbatch run.slurm  benchmarks/MAXSAT_benchmarks/ fouriersat unconstrained_ABS_SLSQP 1 abs SLSQP 1

sbatch run.slurm  benchmarks/MAXSAT_benchmarks/ fouriersat constrained_ABS_GD 0 abs GD 1
sbatch run.slurm  benchmarks/MAXSAT_benchmarks/ fouriersat unconstrained_ABS_GD 1 abs GD 1

sbatch run.slurm  benchmarks/MAXSAT_benchmarks/ fouriersat constrained_SQUARE_GD 0 square GD 1
sbatch run.slurm  benchmarks/MAXSAT_benchmarks/ fouriersat unconstrained_SQUARE_GD 1 square GD 1

sbatch run.slurm  benchmarks/MAXSAT_benchmarks/ fouriersat constrained_LINEAR_GD 0 linear GD 1
sbatch run.slurm  benchmarks/MAXSAT_benchmarks/ fouriersat constrained_LINEAR_SLSQP 0 linear SLSQP 1
"""
sbatch run.slurm  randomInstances/CNF_1000 fouriersat unconstrained_CG 1 square CG 0
sbatch run.slurm  randomInstances/CNF_1000 fouriersat unconstrained_GD 1 square GD 0
sbatch run.slurm  randomInstances/CNF_1000 fouriersat constrained_GD 0 square GD 0
