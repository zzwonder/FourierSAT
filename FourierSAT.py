import scipy.optimize as so
import numpy as np
import time
import random
from boolean_formula import Formula
import signal
import multiprocessing
from functools import partial
from multiprocessor import abortable_worker
import argparse
from util import *
from args import *
from fval import fun
from gradient import gradient
import GSAT
import sgd
import coordinate_descent
import gradient_descent

#update the weights of UNSAT constraints
def verify_sol_update_weights(formula,x,klist,weight,ctype):
    clauses = formula.clauses
    x = rounding(x)
    n = len(x)
    num_of_unsat_clauses = 0
    unsat_weight = 0
    ucnf = 0
    uxor = 0
    for i in range(len(clauses)):
        l_list = clauses[i]
        unsat_flag = 0
        if ctype[i] == 'c':
            if sum(j/abs(j)*x[abs(j)-1] for j in l_list)>len(l_list)-2*klist[i]:
                ucnf += 1
                unsat_flag = 1
        elif ctype[i] == 'x':
            if prod(i/abs(i)*x[abs(i)-1] for i in l_list) > 0:
                unsat_flag = 1
                uxor+=1
        elif ctype[i] == 'n':
            i0 = l_list[0]
            unsat_flag = 1
            v0 = i0/(abs(i0))*x[abs(i0)-1]
            for j in l_list:
                if j/abs(j)*x[abs(j)-1] != v0:
                    unsat_flag = 0
                    break
        if unsat_flag:
            unsat_weight += weight[i]
            num_of_unsat_clauses += 1
            weight[i] += ( ARGS.weight_update_factor * len(l_list))  # update the weights with giving long constriants larger weight
    return num_of_unsat_clauses, unsat_weight, weight

def callback(xk):
    pass
    # callback function for investigating the states of scipy optimizers

def optimizer_handler(clauses,klist,param,weight,ctype,no,FC_table):
    numofvars,numofclas = param
    np.random.seed(ARGS.trial_no)
    x0 = (2 * np.random.rand(numofvars) - 1)
    numofvars,numofclas = param
    args = [clauses, weight, klist, ctype, FC_table]
    if ARGS.optimizer == "GD":
        distFval, contFval, x, iterNum = gradient_descent.gradient_descent(x0, args)
    elif ARGS.optimizer == "GSAT":
        distFval, contFval, x, iterNum = GSAT.GSAT(x0, args)
    # you can use your favorite optimizer here. just return the converged fun(rounding(x)) (distfval), the converged fun(x) (contFval), converged x (x) and number of iterations used (iterNum)
    elif ARGS.optimizer == "SGD":
        distFval, contFval, x, iterNum = sgd.SGD(x0, args)
    elif ARGS.optimizer == "RMSPROP":
        distFval, contFval, x, iterNum = sgd.RMSPROP(x0, args)
    elif ARGS.optimizer == "ADAM":
        distFval, contFval, x, iterNum = sgd.ADAM(x0, args)
    elif ARGS.optimizer == "CD":
        distFval, contFval, x, iterNum = coordinate_descent.coordinate_descent(x0, args)
    else:
        opt = {'maxiter':50,'disp':True}
        if ARGS.unconstrained == 1:  # unconstrained optimization
            res = so.minimize(fun, x0, method=ARGS.optimizer, jac=gradient,args=args, callback=callback, tol=1e-3, options=opt)  #Alternative method: L-BFGS-B tol=0.1
        else:
            bnds = ()
            for j in range(numofvars): bnds += ((-1, 1),) 
            res = so.minimize(fun, x0, method=ARGS.optimizer, bounds=bnds,jac=gradient,args=args,options=opt, callback=callback, tol=1e-3)  #Alternative method: L-BFGS-B tol=0.1
            return {'distFval': res.fun, 'contFval': res.fun, 'x': res.x, 'iterNum': res.nit}
        #res = so.basinhopping(fun, [0 for i in range(numofvars)], minimizer_kwargs = {'args':args})  #Alternative method: L-BFGS-B tol=0.1
        #res = so.direct(fun, args=args, callback=callback)  #Alternative method: L-BFGS-B tol=0.1
        #res = so.dual_annealing(fun, args=args, callback=callback)  #Alternative method: L-BFGS-B tol=0.1
        #res = so.differential_evolution(fun,bounds=bnds, callback=callback,args=args)  #Alternative method: L-BFGS-B tol=0.1
        #res = so.shgo(fun, args=args,callback=callback)  #Alternative method: L-BFGS-B tol=0.1
    return {'distFval': distFval, 'contFval': contFval, 'x':x, 'iterNum': iterNum}


def solve(filepath,timelimit,tolerance,cpus,verbose):
        formula = Formula()
        formula = Formula.read_DIMACS(filepath)
        numofvars = len(formula._variables)
        numofcla = len(formula.clauses)
        param = numofvars, numofcla
        weight = formula._weight
        klist = formula._klist
        comparator = formula._comparator
        ctype = formula._ctype
        coefs = formula._coefs
        FC_table = compute_FC_table(formula.clauses,klist,ctype,coefs,comparator)
        elapsed = 0
        start = time.time()
        bestx = []
        best_unsat_num = numofcla
        total_time_limit = timelimit
        solved_flag = 0
        weight_group = []
        for _ in range(cpus):
            weight_group.append(weight)
        while elapsed < total_time_limit:
            trial_start = time.time()
            results = []
            pool = multiprocessing.Pool()
            for cpu_index in range(cpus):
                time_left = total_time_limit - elapsed 
                increase_ARGS_seed()
                abortable_func = partial(abortable_worker, optimizer_handler,timeout = time_left)
                result = pool.apply_async(abortable_func, args=(formula.clauses,klist,param,weight_group[cpu_index],ctype,cpu_index, FC_table))
                results.append(result)
            pool.close()
            pool.join()
            for cpu_index in range(cpus):
                res = results[cpu_index].get()
                if len(res) == 0 or  len(res['x'])<numofvars:
                    res['x'] = [1 for _ in range(numofvars)]
                num_of_unsat, weight_of_unsat, weight_group[cpu_index] = verify_sol_update_weights(formula, res['x'], klist, weight_group[cpu_index], ctype)
                if num_of_unsat == 0:
                    bestx = res['x']
                    best_unsat_num = 0
                    break
                else:
                    if num_of_unsat < best_unsat_num:
                        bestx = res['x']
                        best_unsat_num = num_of_unsat
                        if ARGS.ismaxsat == 1:
                            print('o '+repr(num_of_unsat))
            print('distFval = ' + repr(num_of_unsat) + ' contFval = ' + repr(res['contFval']) +  ' iterNum = ' + repr(res['iterNum']) + ' time = ' + repr(time.time() - trial_start) + ' TrialNum = ' + repr(ARGS.trial_no) + ' avgIterTime ' + repr((time.time() - trial_start)/res['iterNum']))
            
            if verbose == 1:
                print('#UNSAT clauses: '+repr(best_unsat_num))
            if ARGS.mode == 'solver' and best_unsat_num <= tolerance:
                solved_flag = 1
                print('s Solved at iterNum = ' + repr(res['iterNum']) + ' time = ' + repr(time.time() - trial_start) + ' TrialNum = ' + repr(ARGS.trial_no) + ' avgTimePerIteration ' + repr((time.time() - trial_start)/res['iterNum']))
            
            elapsed = time.time() - start
            if ARGS.trial_no >= ARGS.maxTrial: break
        """
        if solved_flag==0:
            print('s Not Solved in ' + repr(timelimit) + ' seconds. Minimum number of unSAT clauses = ' + repr(best_unsat_num))
            if verbose == 1:
                print_assignment(bestx)
        """

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath',type=str,help='set the file path')
    parser.add_argument('--timelimit', type=int, help='set the time limit (seconds) default: 60', default=60)
    parser.add_argument('--tolerance',type=int, help='set the number of clauses allowed to be unsatisfied, default: 0', default=0)
    parser.add_argument('--cpus',type=int,help='set the number of cores, default: 1', default=1)
    parser.add_argument('--ismaxsat',type=int,help='set to 1 if solving unweighted MAXSAT problem, default 0',default=0)
    parser.add_argument('--verbose',type=int,help='set verbose to 1 to output more information, default: 0',default=0)
    parser.add_argument('--unconstrained',type=int,help='set to 1 to use unconstrained optimization, default: 0',default=0)
    parser.add_argument('--objectiveType',type=str,help='the type of continuous objective function, {linear,  abs, square}, default: square',default='square')
    parser.add_argument('--beta',type=float,help='the factor applied on the (1-x^2) term in the global optimization version, default: 0',default=0)
    parser.add_argument('--weight_update_factor',type=float,help='the factor of the original weights applied to an UNSAT constraint, default: 0',default=0)
    parser.add_argument('--optimizer',type=str,help='the optimizer, selected from {SLSQP, CG, GD, CD}, default: SLSQP. GD: gradient descent, CD: coordinate descent',default='SLSQP')
    parser.add_argument('--maxTrial', type=int, help='max number of trials of optmization. default: 10', default = 10)
    parser.add_argument('--mode', type=str, help='[solver] mode or [dev]eloper mode', default='dev')
    args = parser.parse_args()
    if not args.filepath:
        print('Please provide a filepath!')
        exit(0)
    setArgs(objectiveType=args.objectiveType, beta=args.beta, weight_update_factor=args.weight_update_factor, optimizer = args.optimizer, unconstrained = args.unconstrained, ismaxsat = args.ismaxsat, maxTrial = args.maxTrial, mode = args.mode)
    solve(args.filepath,args.timelimit,args.tolerance,args.cpus,args.verbose)
if __name__ == "__main__":
    main()
