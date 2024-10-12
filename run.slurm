#!/bin/bash
#SBATCH --job-name=maxsat
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=1000m
#SBATCH --cpus-per-task=1
#SBATCH --time=23:59:59
#SBATCH --nodes=1
#SBATCH --partition=commons
#SBATCH --profile=ALL
#SBATCH --error=error_messages/%j.out
#module load Anaconda3/5.0.0
#module load GCC/8.3.0
#module load OpenMPI/3.1.4
#module load SciPy-bundle/2019a

function run(){
TL=6000
NC=1

mkdir -p results_2024/$3
for file in `ls $1`
do
    if [ -d $1"/"$file ] 
    then
        run $1"/"$file $2 $3 $4 $5 $6 $7 $8 $9
    else
        filename=$(basename $1"/"$file)
        #if [[ $filename != *.cnf ]]
        #then 
        #    continue 
        #fi
        filepath=$1/$file
        echo $file
	start=$(date +%s)
        outpath="res/$2.txt"
        if [[ $2 == 'cms' ]];
        then
            timeout $TL cryptominisat5 $filepath  > /dev/null 2>&1
	elif [[ $2 == 'naps' ]];
	then
            timeout $TL ../binary_of_other_solvers/naps  $filepath 
	elif [[ $2 == 'roundingsat' ]];
	then
            timeout $TL ../binary_of_other_solvers/roundingsat < $filepath 
	elif [[ $2 == 'openwbo' ]];
	then
            timeout $TL ../open-wbo/open-wbo -formula=1 $filepath 
        elif [[ $2 == 'fouriersat' ]];
        then
            #timeout $TL python FourierSAT.py --timelimit $TL --globalopt 0 --ismaxsat 1 --beta 0 --globalmode square --weight_update_factor 0 --optimizer SLSQP $filepath > res_$3/${file}.txt
            if [ -f results_2024/$3/${file}.txt ]
            then continue
            else
                timeout $TL python FourierSAT.py --timelimit $TL --unconstrained $4 --objectiveType $5 --optimizer $6 --ismaxsat $7 --beta $8 --mode $9 $filepath > results_2024/$3/${file}.txt
            fi
        else 
            timeout $TL solvers_binary/$2 $filepath > /dev/null 2>&1
	fi
    fi
done 
}


#run randomInstances/XOR_1000 fouriersat unconstrained_SLSQP
#run benchmarks/MAXSAT_benchmarks/ fouriersat unconstrained_GD
#run $1 $2 $3
run $1 $2 $3 $4 $5 $6 $7 $8 $9
