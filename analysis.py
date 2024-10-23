import os
import matplotlib.pyplot as plt
import numpy as np

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

# analyze the penalty term
def analyze_solver(benchmark, names):
    benchmarks = os.listdir(benchmark)
    results = {}
    
    #solvers_temp = ["SLSQP_0.0", "SLSQP_0.2","SLSQP_0.4","SLSQP_0.6", "SLSQP_0.8", "SLSQP_1.0", "SLSQP_1.2", "SLSQP_1.4", "SLSQP_1.6", "SLSQP_1.8"]
    solvers_temp = ["ADAM_0.0", "ADAM_0.2","ADAM_0.4","ADAM_0.6", "ADAM_0.8", "ADAM_1.0", "ADAM_1.2", "ADAM_1.4", "ADAM_1.6", "ADAM_1.8"]
    for name in names:
        if name == "penaltyTermABS":
            solvers = ["unconstrained_ABS_" + s for s in solvers_temp]
            r = [0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8]
        elif name == "penaltyTermSQUARE":
            solvers = ["unconstrained_SQUARE_" + s for s in solvers_temp]
            r = [0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8]
        elif name == "penaltyTermABS-C":
            solvers = ["constrained_ABS_" + s for s in solvers_temp]
            r = [0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8]
        elif name == "penaltyTermSQUARE-C":
            solvers = ["constrained_SQUARE_" + s for s in solvers_temp]
            r = [0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8]

        elif name == "formulation_SLSQP":
            r = ["SLSQP-ABS-C", "SLSQP-SQUARE-C","SLSQP-LINEAR-C", "SLSQP-SQUARE", "SLSQP-ABS"]
            solvers = ["constrained_ABS_SLSQP", "constrained_SQUARE_SLSQP","constrained_LINEAR_SLSQP", "unconstrained_SQUARE_SLSQP", "unconstrained_ABS_SLSQP"]
            solvers = ["constrained_ABS_SLSQP_0.0", "constrained_SQUARE_SLSQP_0.0","constrained_LINEAR_SLSQP", "unconstrained_SQUARE_SLSQP_0.8", "unconstrained_ABS_SLSQP_0.8"]
        elif name == "formulation_GD":
            r = ["GD-ABS-C", "GD-SQUARE-C","GD-LINEAR-C", "GD-SQUARE", "GD-ABS"]
            #solvers = ["constrained_ABS_GD", "constrained_SQUARE_GD","constrained_LINEAR_GD", "unconstrained_SQUARE_GD", "unconstrained_ABS_GD"]
            solvers = ["constrained_ABS_GD", "constrained_SQUARE_GD","constrained_LINEAR_GD", "unconstrained_SQUARE_GD_0.8", "unconstrained_ABS_GD_0.8"]

        for solver in solvers:
            results[solver] = []
            for instance in benchmarks:
               try:
                   f = open("results_2024/" + solver + "/" + instance + ".txt", "r+")
                   lines = f.readlines()
                   for line in lines:
                       split = line.split()
                       if len(split) == 0: continue
                       if split[0] == "s":
                           results[solver].append(instance)
                           break 
               except Exception as err: continue
        solvedInstances = []
        for solver in solvers: 
            print(solver, len(results[solver]))
            solvedInstances.append(len(results[solver]))
            
        r = [0,0.2,0.4,0.6,0.8,1.0]
        solvedInstances = solvedInstances[:len(r)]        
        fig, ax = plt.subplots()
        x = np.arange(len(r))
        ax.bar(x,[ solvedInstance * 1.0 / len(benchmarks) for solvedInstance in solvedInstances])
        print([ solvedInstance * 1.0 / len(benchmarks) for solvedInstance in solvedInstances])
        ax.set_xticks(x)
        ax.set_xticklabels(r,fontsize=10)
        plt.savefig("figs/" + name + '_' + problem + '.png')
        plt.cla()
        ax.set_ylim((0,1))
        ax.set_ylabel('raito of solved problems')
        ax.set_xlabel('penalty coef.')
        print('saved one figure')
    #plt.legend(solvers)

# histgram drawing for cnfxorcard 
def drawHist():
    r = [0,0.2,0.4,0.6,0.8, 1.0]
    res_sq_adam = [0.47, 0.89, 0.905, 0.93, 0.9666, 0.96]
    res_sq_slsqp = [0.13, 0.68, 0.71, 0.752, 0.8, 0.76] 
    width = 0.35
    fig, ax = plt.subplots()
    x = np.arange(len(r))
    rects1 = ax.bar(x - width/2, res_sq_adam, width, label='ADAM_SQ')
    rects2 = ax.bar(x + width/2, res_sq_slsqp, width, label='SLSQP_SQ')
    ax.set_xticks(x)
    ax.set_xticklabels(r)
    ax.set_ylabel('ratio of solved problems', fontsize = 15)
    ax.set_xlabel('barrier coefficient', fontsize = 15)
    ax.set_xticklabels(r,fontsize=12)
    ax.legend(fontsize = 13)
    plt.savefig("figs/" + 'penaltyCard' + '.png')
    plt.cla()

def analyze_thesis(benchmark = "CNF_1000", figDir = "figs/", name=""):
    results = {}
    successTrials = {}
    solvers = []    
    solversMap = {"constrained_ABS_SLSQP":"SLSQP-ABS-C", "unconstrained_SQUARE_GD":"GD-SQ", "unconstrained_SQUARE_ADAM":"ADAM-SQ", "unconstrained_SQUARE_SLSQP":"SLSQP-SQ", "constrained_SQUARE_SLSQP":"SLSQP-SQ-C", "constrained_SQ_GD":"GD-SQUARE-C", "unconstrained_ABS_GD":"GD-ABS","unconstrained_ABS_SLSQP":"SLSQP-ABS","constrained_ABS_GD":"GD-ABS-C","constrained_ABS_SLSQP":"SLSQP-ABS-C", "constrained_LINEAR_SLSQP":"SLSQP-LIN-C", "constrained_LINEAR_GD":"GD-LIN-C", "constrained_SQUARE_GD":"GD-SQ-C"}
   
    if benchmark == "CNF_1000": Range = range(10,40,2)
    elif benchmark == "XOR_1000": Range = range(1,6,1)
    if name == "SLSQP": 
        solvers = ["constrained_LINEAR_SLSQP", "constrained_SQUARE_SLSQP", "unconstrained_SQUARE_SLSQP"]
    elif name == "GD": 
        solvers = [ "constrained_LINEAR_GD", "constrained_SQUARE_GD", "constrained_ABS_GD", "unconstrained_SQUARE_GD"]
    elif name == "diffAlgo": 
        solvers = ["constrained_ABS_SLSQP","constrained_LINEAR_GD","unconstrained_SQUARE_GD", "unconstrained_SQUARE_ADAM", "unconstrained_SQUARE_SLSQP", "constrained_SQUARE_SLSQP", "constrained_SQUARE_GD", "unconstrained_ABS_GD","unconstrained_ABS_SLSQP","constrained_ABS_GD", "constrained_LINEAR_SLSQP"]
    elif name == "formulation_SLSQP":
        solvers = ["constrained_ABS_SLSQP", "constrained_SQUARE_SLSQP","constrained_LINEAR_SLSQP", "unconstrained_SQUARE_SLSQP", "unconstrained_ABS_SLSQP"]
    elif name == "formulation_GD":
        solvers = ["constrained_ABS_GD", "constrained_SQUARE_GD","constrained_LINEAR_GD", "unconstrained_SQUARE_GD", "unconstrained_ABS_GD"]
    elif name == "penaltyTermABS":
        solvers = ["unconstrained_ABS_SLSQP_0.0", "unconstrained_ABS_SLSQP_0.2","unconstrained_ABS_SLSQP_0.4","unconstrained_ABS_SLSQP_0.6","unconstrained_ABS_SLSQP_0.8"]
    elif name == "penaltyTermSQUARE":
        solvers = ["unconstrained_SQUARE_SLSQP_0.0", "unconstrained_SQUARE_SLSQP_0.2","unconstrained_SQUARE_SLSQP_0.4","unconstrained_SQUARE_SLSQP_0.6","unconstrained_SQUARE_SLSQP_0.8"]

    elif name == "penaltyTermABS-C":
        solvers = ["constrained_ABS_SLSQP_0.0", "constrained_ABS_SLSQP_0.2","constrained_ABS_SLSQP_0.4","constrained_ABS_SLSQP_0.6","constrained_ABS_SLSQP_0.8"]
    elif name == "penaltyTermSQUARE-C":
        solvers = ["constrained_SQUARE_SLSQP_0.0", "constrained_SQUARE_SLSQP_0.2","constrained_SQUARE_SLSQP_0.4","constrained_SQUARE_SLSQP_0.6","constrained_SQUARE_SLSQP_0.8"]

    for solver in solvers: 
        results[solver] = []
        successTrials[solver] = []
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
                results[solver].append(round(success_rate * 1.0 / trials,2))
                successTrials[solver].append(trials)
        print(solver)
        print(results[solver])
        print(successTrials[solver])
        #plt.plot(Range, results[solver])   
    
    if "penalty" in name: 
        r = [0,0.2,0.4,0.6,0.8]
        fig, ax = plt.subplots()
        for solver in solvers:
            ax.plot([k/10 for k in Range], results[solver], linewidth=3)
        ax.set_ylabel('ratio of solved instances',fontsize=16)
        ax.set_xlabel('clause-vairable ratio',fontsize=16)
        ax.tick_params(axis='both', which='major', labelsize=12)

        ax.legend(r, fontsize=16)
        plt.savefig(figDir + benchmark + '_' + name + '.png')
        plt.cla()
    elif "diff" in name:
        fig, ax = plt.subplots()
        solverRank = []
        for solver in solvers:
            solverRank.append(sum(results[solver]))
        order = sorted(range(len(solverRank)), key=lambda k: solverRank[k])[::-1]
        ax.set_ylabel('ratio of solved instances',fontsize=16)
        ax.set_xlabel('clause-vairable ratio',fontsize=16)
        for idx in order:
            ax.plot([k/10 for k in Range], results[solvers[idx]], linewidth=3)
        ax.legend([ solversMap[solvers[idx]] for idx in order])
        plt.savefig(figDir + benchmark + '_' + name + '.png')
        plt.cla()

    elif "formulation" in name:
        if problem == "CNF_1000" or problem == "XOR_1000":
            fig, ax = plt.subplots()
            solverRank = []
            for solver in solvers:
                if solver in results:
                    solverRank.append(sum(results[solver]))
            order = sorted(range(len(solverRank)), key=lambda k: solverRank[k])[::-1]
            
            for idx in order:
                if "SQUARE" in solvers[idx]: color = 'b'
                if "ABS" in solvers[idx]: color = 'orange'
                if "LINEAR" in solvers[idx]: color = 'g'
                lineshape = '--' if "unconstrained" in solvers[idx] else '-'
                ax.plot([k/10 for k in Range], results[solvers[idx]], linewidth=3, color=color, linestyle=lineshape)   
            ax.set_ylabel('ratio of solved instances',fontsize=16)
            ax.set_xlabel('clause-vairable ratio',fontsize=16)
            ax.tick_params(axis='both', which='major', labelsize=12)
            ax.legend([ solversMap[solvers[idx]] for idx in order])
            plt.savefig(figDir + benchmark + '_' + name + '.png')
            plt.cla()
        elif problem == "CNFXORCARD":
            pass

def analyze_thesis_maxsat(folder):
    results = {}
    #solvers = ["unconstrained_GD", "constrained_GD", "unconstrained_SLSQP", "unconstrained_CG", "constrained_SLSQP", "unconstrained_LBFGSB", "constrained_LBFGSB", "constrained_ABS_SLSQP", "constrained_SQUARE_SLSQP", "unconstrained_ABS_SLSQP", "constrained_SQUARE_GD", "constrained_ABS_GD"]
    #solvers = ["unconstrained_SQUARE_SLSQP", "unconstrained_SQUARE_GD", "constrained_ABS_SLSQP", "constrained_SQUARE_SLSQP", "unconstrained_ABS_SLSQP", "constrained_SQUARE_GD", "constrained_ABS_GD"]
    #solvers = ["unconstrained_SQUARE_SLSQP", "constrained_LINEAR_SLSQP", "constrained_ABS_SLSQP", "constrained_SQUARE_SLSQP", "unconstrained_ABS_SLSQP", "constrained_SQUARE_GD", "constrained_ABS_GD"]
    #solvers = ["constrained_SQUARE_SLSQP", "constrained_LINEAR_SLSQP", "unconstrained_SQUARE_GD", "constrained_ABS_GD"]
    solvers = ["constrained_CE_SLSQP", "constrained_LINEAR_SLSQP", "constrained_SQUARE_GD", "constrained_ABS_GD"]
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

#problems = ["XOR_1000"] 
problems = ["CNF_1000", "XOR_1000"] 
#problems = ["cards"]
#problems = ["cnfxorcard"] 
#names = ["diffAlgo","formulation_SLSQP", "formulation_GD"]
names = ["formulation_SLSQP", "formulation_GD"]
names = ["formulation_GD"]
names = ["diffAlgo"]
#names = ["penaltyTermABS", "penaltyTermSQUARE", "penaltyTermABS-C", "penaltyTermSQUARE-C"]
# figure 5
drawHist()

for problem in problems:
    for name in names:
        analyze_thesis(benchmark = problem, name = name)
        #analyze_thesis_maxsat("/benchmarks/MAXSAT_benchmarks/")
        #analyze_solver(benchmark = "benchmarks/cnfxorcard/new/", names = [name])
        #analyze_solver(benchmark = "benchmarks/cards/", names = [name])
