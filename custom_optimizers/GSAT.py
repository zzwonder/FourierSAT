# GSAT (greedy local search)
from ../gradient.py import gradient
def GSAT(x0, args):
    fval_best = 1e10
    maxIter = 10000
    x = rounding(x0)
    distFval = 1e10
    iterNum = 1
    while iterNum < maxIter:
        grad = gradient(x, args)
        for i in range(len(x)):
            if grad[i] * x[i] <= 0: grad[i] = 0
            else: grad[i] = abs(grad[i])
        ind = np.argmax(grad)
        x[ind] *= (-1)
        distFval = fun(x,args)
        if distFval < 1e-3: break
        if grad[ind] < 1e-3: break
        iterNum += 1
        print("iter " + repr(iterNum) + " distFval " + repr(distFval)) # + " time " + repr(time.time()))
    return distFval, distFval, x, iterNum
