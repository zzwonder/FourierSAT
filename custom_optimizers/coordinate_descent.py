# coordinate descent in the continuous domain. Each iteration, all coordinates are fixed except for one. The problem left is a quadratic optimization problem
from ../gradient.py import gradient
def minimize_quadratic(x, i, args):
    eps = 1e-3
    x1 = [xi for xi in x]
    x1[i] += eps
    grad1 = (fun_global(x1, args) - fun_global(x, args)) / eps

    x2 = [xi for xi in x]
    x2[i] += 0.5
    x3 = [xi for xi in x2]
    x3[i] += eps
    grad2 = (fun_global(x3, args) - fun_global(x2, args)) /eps

    a = (grad2 - grad1)
    b = grad1 - 2 * a * x1[i]
    if abs(grad1) < 1e-4 and abs(grad2) < 1e-4: return x[i]
    return -b/(2*a)

def coordinate_descent(x0, args):
    x = x0.copy()
    maxIter = 10000
    iterNum = 1
    distFval = 1e10
    contFval = 1e10
    while iterNum < maxIter:
        for i in range(len(x)):
            x[i] = minimize_quadratic(x, i,args)
            contFval = fun(x, args)
            distFval = fun(rounding(x), args)
            print("iter " + repr(iterNum) + " distFval " + repr(distFval) + " contFval " + repr(contFval)) # + " time " + repr(time.time()))
            if distFval < 1e-2: break
            iterNum += 1
    return distFval, fval_final, x_final, iterNum
