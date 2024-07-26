import os
import matplotlib.pyplot as plt

def getAllFileName(folder):
    allFiles = []
    for path, subdirs, files in os.walk(folder):
        for name in files:
            allFiles.append(name)
    return allFiles

def getList(solverName, allFiles):
    res = {}
    for problem in allFiles:
        try: 
            f = open(solverName + "/" + problem + ".txt")
            lines = f.readlines()
            for i in range(len(lines)-1, 0, -1):
                if len(lines[i]) > 0:
                    split = lines[i].split()
                    if split[0] == "o":
                        res[problem] = int(split[1])
                        break
        except FileNotFoundError: pass
        if problem not in res.keys(): res[problem] = 99999
    return res


def analyze_thesis(benchmark = "CNF_1000", Range = range(10,36,2)):
    results = {}
    solvers = ["unconstrained_GD", "constrained_GD", "unconstrained_SLSQP", "unconstrained_CG", "constrained_SLSQP", "unconstrained_LBFGSB", "constrained_LBFGSB", "constrained_ABS_SLSQP", "constrained_SQUARE_SLSQP", "unconstrained_ABS_SLSQP", "constrained_SQUARE_GD", "constrained_ABS_GD"]
    
    for solver in solvers: 
        results[solver] = []
        for alpha10 in Range:
            success_rate = 0
            trials = 0
            for i in range(10):
               try:
                   f = open("results_2024/" + solver + "/" + benchmark + "_" + repr(alpha10 * 1.0/10) + "_" + repr(i) + ".txt.txt", "r+")
                   lines = f.readlines()
                   for line in lines:
                       split = line.split()
                       if len(split) == 0: continue
                       if split[0] == "distFval":
                           trials += 1
                           distFval = int(split[2])
                           if distFval == 0: 
                               success_rate += 1 
               except Exception as err: continue
            if trials == 0: results[solver].append(0)
            else:
                results[solver].append(success_rate * 1.0 / trials)
        print(solver)
        print(results[solver])
        plt.plot(results[solver])  
    plt.legend(solvers)
    plt.savefig('res.png')

def analyze_thesis_maxsat(folder):
    results = {}
    #solvers = ["unconstrained_GD", "constrained_GD", "unconstrained_SLSQP", "unconstrained_CG", "constrained_SLSQP", "unconstrained_LBFGSB", "constrained_LBFGSB", "constrained_ABS_SLSQP", "constrained_SQUARE_SLSQP", "unconstrained_ABS_SLSQP", "constrained_SQUARE_GD", "constrained_ABS_GD"]
    #solvers = ["unconstrained_SQUARE_SLSQP", "unconstrained_SQUARE_GD", "constrained_ABS_SLSQP", "constrained_SQUARE_SLSQP", "unconstrained_ABS_SLSQP", "constrained_SQUARE_GD", "constrained_ABS_GD"]
    solvers = ["unconstrained_SQUARE_SLSQP", "constrained_ABS_SLSQP", "constrained_SQUARE_SLSQP", "unconstrained_ABS_SLSQP", "constrained_SQUARE_GD", "constrained_ABS_GD"]
    allFiles = getAllFileName("benchmarks/MAXSAT_benchmarks")
    for solver in solvers:
        results[solver] = {}
        for instance in allFiles:
            best = 10000
            for i in range(10):
               try:
                   f = open("results_2024/" + solver + "/"  + instance + ".txt", "r+")
                   lines = f.readlines()
                   
                   for line in lines:
                       split = line.split()
                       if len(split) == 0: continue
                       if split[0] == "distFval":
                           distFval = int(split[2])
                           if distFval < best:    best = distFval
               except Exception as err: continue
            results[solver][instance] = best
    
    allsolved = []
    for instance in allFiles:
        solvedFlag = 1
        for solver in solvers:
            if results[solver][instance] == 10000:
                solvedFlag = 0
                break
        if solvedFlag == 1: 
            allsolved.append(instance)
            print(instance)
    print(len(allsolved))

    score = {}
    for solver in solvers: score[solver] = 0
    for instance in allsolved:
        best = 10000
        for solver in solvers:
            if results[solver][instance] < best: best = results[solver][instance]
        for solver in solvers:
            score[solver] += (1+best) * 1.0 / (1+results[solver][instance])    
    with open("maxsat_res.txt", "w+") as f:
        for solver in solvers:
            f.write(solver + "\t")
        f.write("\n")
        for instance in allFiles:
            for solver in solvers:
                f.write(repr(results[solver][instance]) + "\t")
            f.write("\n")
    for solver in solvers:
       print(solver)
       print(score[solver] / len(allsolved)) 



def analyze():
    solvers = ["res_constrained", "res_constrained_updatefactor_1", "res_unconstrained", "res_unconstrained_abs", "res_unconstrained_abs_beta_0.5", "res_unconstrained_abs_beta_0.5_updatefactor_1", "res_unconstrained_beta_0.5", "res_unconstrained_beta_0.5_updatefactor_1", "res_unconstrained_new", "res_unconstrained_new_SLSQP", "res_unconstrained_new_updatefactor_1"]
    allres = {}
    allFiles = getAllFileName("benchmarks/MAXSAT_benchmarks")
    for solver in solvers:
        allres[solver] = getList(solver, allFiles)
    with open("result.txt", "w+") as f:
       print("\t")
       for solver in solvers:
           f.write(solver + "\t")
       f.write("\n") 
       for problem in allFiles:
            f.write(problem + "\t")
            for solver in solvers:
                f.write(repr(allres[solver][problem]) + "\t")
            f.write("\n")
    print("finish getting all res")
    best = {}
    for problem in allFiles:
        bestres = 99999
        for solver in solvers:
            if bestres > allres[solver][problem]: bestres = allres[solver][problem]
        best[problem] = bestres
    realbest = {}
    with open("best.txt", "r+") as f:
        lines = f.readlines()
        for line in lines:
            if len(line) == 0: continue
            split = line.split()
            if len(split) != 4: continue
            if split[1] == "O": realbest[split[0]] = int(split[3])        
    realbest["readme.txt"] = 99999

    for solver in solvers:
        totalScore = 0
        for problem in allFiles:
            totalScore += ( (realbest[problem] + 1 ) / (allres[solver][problem] + 1) )
        totalScore /= len(allFiles)
        print(solver)
        print(totalScore)
            
         
analyze_thesis("CNF_1000", range(10,38,2))
#analyze_thesis("XOR_1000", range(1,10,1))
#analyze_thesis_maxsat("/benchmarks/MAXSAT_benchmarks/")
