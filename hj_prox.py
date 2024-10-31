# vanilla HJ_prox
from fval import fun
from HJ_utils import compute_prox, compute_prox_parallel
from util import *
from args import *
from SAT2poly import SAT2PolyStr
import torch

def hj_prox(x0, args):
    fval_best = 1e10
    maxIter = int(1e4)
    x = x0
    eps = 1e-4
    distFval = 1e10
    contFval = 1e10
    iterNum = 0
    # if ARGS.ismaxsat == 1: eps = 5e-5 * len(x0)

    dist_fval_best = 1e10
    cont_fval_best = 1e10
    # while iterNum < maxIter:
    #     print('STARTING OPTIMIZER')
    #     # if ARGS.optimizer == "HJPROX_PARALLEL":
    #     #     polystr = SAT2PolyStr(args, len(x0), objectiveType = ARGS.objectiveType, beta = ARGS.beta)
    #     #     #print(polystr)
    while iterNum < maxIter:
        if ARGS.optimizer == "HJPROX_PARALLEL":
            polystr = SAT2PolyStr(args, len(x0), objectiveType = ARGS.objectiveType, beta = ARGS.beta)
            x, *_ = compute_prox_parallel(x, polystr, t=1e-1, delta=1e-1, int_samples=int(1e5), alpha=1.0, linesearch_iters=0)
        elif ARGS.optimizer == "HJPROX":
            x, *_ = compute_prox(x, args, fun, t=1e-1, delta=1e-2, int_samples=int(1e4), alpha=1.0, linesearch_iters=0)
        if not ARGS.unconstrained:
            x = truncate(x)
        contFval = fun(x, args)
        x = torch.tensor(x).view(1,-1)
        contFval2 = eval(polystr)
        x = x.view(-1, ).numpy()
        # print('iter ' + repr(iterNum), 'contFval = ', contFval, ', contFval using PolyStr = ', contFval2)
        distFval = fun(rounding(x), args)
        if distFval < dist_fval_best:
            x_best = x
        dist_fval_best = min(dist_fval_best, distFval)
        cont_fval_best = min(cont_fval_best, contFval)
        if distFval < 1: break
        iterNum += 1
        # print("iter " + repr(iterNum) + " distFval " + repr(distFval) + " contFval " + repr(contFval)) # + " time " + repr(time.time()))
        print('iter ' + repr(iterNum), 'contFval = ', contFval, ', contFval using PolyStr = ', contFval2)
    return dist_fval_best, cont_fval_best, x_best, iterNum
