#code is based on https://gist.github.com/jcmgray/e0ab3458a252114beecb1f4b631e19ab

import numpy as np
from scipy.optimize import OptimizeResult
from gradient import gradient
from fval import fun
from args import *
from util import *


def SGD(x0, args):
    res = sgd(fun, x0, gradient, args = args)
    return fun(rounding(res.x), args), fun(res.x, args), res.x, res.nit

def RMSPROP(x0, args):
    res = rmsprop(fun, x0, gradient, args = args)
    return fun(rounding(res.x), args), fun(res.x, args), res.x, res.nit

def ADAM(x0, args):
    res = adam(fun, x0, gradient, args = args)
    return fun(rounding(res.x), args), fun(res.x, args), res.x, res.nit

def sgd(
    fun,
    x0,
    jac,
    args=(),
    learning_rate=0.01,
    mass=0.9,
    startiter=0,
    maxiter=1000,
    callback=None,
    **kwargs
):
    """``scipy.optimize.minimize`` compatible implementation of stochastic
    gradient descent with momentum.
    Adapted from ``autograd/misc/optimizers.py``.
    """
    x = x0
    velocity = np.zeros_like(x)

    for i in range(startiter, startiter + maxiter):
        g = jac(x, args)

        if callback and callback(x):
            break

        velocity = mass * velocity - (1.0 - mass) * g
        x = x + learning_rate * velocity

    i += 1
    return OptimizeResult(x=x, fun=fun(x, args), jac=g, nit=i, nfev=i, success=True)


def rmsprop(
    fun,
    x0,
    jac,
    args=(),
    learning_rate=0.1,
    gamma=0.9,
    eps=1e-8,
    startiter=0,
    maxiter=1000,
    callback=None,
    **kwargs
):
    """``scipy.optimize.minimize`` compatible implementation of root mean
    squared prop: See Adagrad paper for details.
    Adapted from ``autograd/misc/optimizers.py``.
    """
    x = x0
    avg_sq_grad = np.ones_like(x)

    for i in range(startiter, startiter + maxiter):
        g = jac(x, args)

        if callback and callback(x):
            break

        avg_sq_grad = avg_sq_grad * gamma + g**2 * (1 - gamma)
        x = x - learning_rate * g / (np.sqrt(avg_sq_grad) + eps)

    i += 1
    return OptimizeResult(x=x, fun=fun(x, args), jac=g, nit=i, nfev=i, success=True)


def adam(
    fun,
    x0,
    jac,
    args=(),
    learning_rate=0.05,
    beta1=0.9,
    beta2=0.999,
    eps=1e-8,
    startiter=0,
    maxiter=1000,
    callback=None,
    **kwargs
):
    """``scipy.optimize.minimize`` compatible implementation of ADAM -
    [http://arxiv.org/pdf/1412.6980.pdf].
    Adapted from ``autograd/misc/optimizers.py``.
    """
    x = x0
    m = np.zeros_like(x)
    v = np.zeros_like(x)

    for i in range(startiter, startiter + maxiter):
        g = jac(x, args)

        if callback and callback(x):
            break

        m = (1 - beta1) * g + beta1 * m  # first  moment estimate.
        v = (1 - beta2) * (g**2) + beta2 * v  # second moment estimate.
        mhat = m / (1 - beta1**(i + 1))  # bias correction.
        vhat = v / (1 - beta2**(i + 1))
        x = x - learning_rate * mhat / (np.sqrt(vhat) + eps)
        distfval = fun(rounding(x), args)       
        fval = fun(x, args)       
        print("fval", fval, "distfval", distfval)
        if distfval < 1: break
    i += 1
    return OptimizeResult(x=x, fun=fun(x, args), jac=g, nit=i, nfev=i, success=True)
