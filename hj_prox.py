# vanilla HJ_prox
from fval import fun
from HJ_utils import compute_prox, compute_prox_parallel
from util import *
from args import *
from SAT2poly import SAT2PolyStr
import torch

# set default type to double precision
torch.set_default_dtype(torch.float64)

def hj_prox(x0, args):
    fval_best = 1e10
    maxIter = int(1e5)

    dim = len(x0) # assumes x0 is a numpy array
    x = torch.tensor(x0).view(1,dim)
    x_cont = x.clone()
    eps = 1e-4
    distFval = 1e10
    contFval = 1e10
    iterNum = 0
    # if ARGS.ismaxsat == 1: eps = 5e-5 * len(x0)

    t = 1.0
    delta = 1e-1
    int_samples = int(1e4)

    # print('t = ', t, 'delta = ', delta, 'int_samples = ', int_samples)

    dist_fval_best = 1e10
    cont_fval_best = 1e10
    while iterNum < maxIter:
        if ARGS.optimizer == "HJPROX_PARALLEL":
            polystr = SAT2PolyStr(args, len(x0), objectiveType = ARGS.objectiveType, beta = ARGS.beta)

            x = x_cont.clone()
            
            x, *_ = compute_prox_parallel(x, polystr, t=t, delta=delta, int_samples=int_samples, alpha=1.0, linesearch_iters=0)
            contFval = eval(polystr).detach().cpu().item()

            x_cont = x.clone()
            x = torch.sign(x)
            distFval = eval(polystr).detach().cpu().item()

        # elif ARGS.optimizer == "HJPROX":
            # x, *_ = compute_prox(x, args, fun, t=t, delta=delta, int_samples=int_samples, alpha=1.0, linesearch_iters=0)

        distFval = distFval.numpy().detach().cpu().item()
        contFval = contFval.numpy().detach().cpu().item()
        
        if distFval < dist_fval_best:
            x_best = (torch.sign(x).clone().view(-1).detach().cpu().numpy())
        dist_fval_best = min(dist_fval_best, distFval)
        cont_fval_best = min(cont_fval_best, contFval)
        if dist_fval_best < 1: break
        iterNum += 1
        print("iter " + repr(iterNum) + " distFval " + repr(dist_fval_best) + " contFval " + repr(cont_fval_best)) # + " time " + repr(time.time()))
    return dist_fval_best, cont_fval_best, x_best, iterNum
