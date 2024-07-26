# vanilla gradient descent
from ../gradient.py import gradient
from ../fval.py import fun
def gradient_descent(x0, args):
    fval_best = 1e10
    maxIter = 1000
    x = [x0_i for x0_i in x0]
    step_size = 5e-2
    eps = 1e-8
    distFval = 1e10
    contFval = 1e10
    iterNum = 1
    if ARGS.ismaxsat == 1: eps = 5e-5 * len(x0)
    while iterNum < maxIter:
        if not ARGS.unconstrained:
            oldx = x.copy()
            grad = gradient(x, args)
            x = [x[i] - grad[i] * step_size for i in range(len(x))]
            x = truncate(x)
            contFval = fun(x, args)
            if norm([x[i] - oldx[i] for i in range(len(x))]) < eps: break
        else:
            grad = gradient(x, args)
            if norm(grad) < eps: break
            x = [x[i] - grad[i] * step_size for i in range(len(x))]
            contFval = fun(x, args)
        distFval = fun(rounding(x), args)
        print("iter " + repr(iterNum) + " distFval " + repr(distFval) + " contFval " + repr(contFval)) # + " time " + repr(time.time()))
        if distFval < 1/64 and ARGS.objectiveType == "square": break
        iterNum += 1
    return distFval, contFval, x, iterNum
