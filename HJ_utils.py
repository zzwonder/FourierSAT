import torch 
import numpy as np
from args import *

def compute_prox(x, f, t=1e-1, delta=1e-2, int_samples=int(1e4), alpha=1.0, linesearch_iters=0):
    '''
        compute prox.
        input is a single vector x of size (n,)
    '''
    assert x.ndim == 1
    linesearch_iters += 1
    standard_dev = np.sqrt(delta * t / alpha)

    dim = x.shape[0]

    # Sample y from normal distribution centered at x with variance proportional to standard_dev
    y = standard_dev * np.random.randn(int_samples, dim) + x  # y has shape (n_samples x dim)

    # Compute weights for softmax
    z = np.zeros(int_samples)
    f_array = np.zeros(int_samples)
    for i in range(int_samples):
        f_array[i] = f(y[i, :], args) # Compute f(y) for each sample
        # z[i] = -f_array[i] * (alpha / delta)  # Compute f(y) for each sample
    z = -f_array * (alpha / delta)  
    max_z = np.max(z)  # To handle numerical stability for softmax
    z = z[:, None] - max_z  # Subtracting max for numerical stability
    w = np.exp(z) / np.sum(np.exp(z))  # softmax operation, shape = n_samples

    # Check for overflow in softmax
    if not np.isfinite(w).all():
        print('x = ', x)
        print('z = ', z)
        print('w = ', w)
        alpha = 0.5 * alpha
        return compute_prox(x, t, f, delta=delta, int_samples=int_samples, alpha=alpha, linesearch_iters=linesearch_iters)
    else:
        prox_term = np.dot(w.T, y)  # Weighted average of y, shape = (dim,)

        # find index where z is minimum and obtain minimum between f(y_min) and f(prox_term)
        min_index = np.argmin(f_array)
        f_prox = f(prox_term, args)
        if z[min_index] < f_prox:
            prox_term = y[min_index,:]


        # Check for overflow in prox_term
        if not np.isfinite(prox_term).all():
            print('prox overflowed: ', prox_term)
        assert np.isfinite(prox_term).all()

        # Compute envelope
        # envelope = f(prox_term, args) + (1 / (2 * t)) * np.linalg.norm(prox_term - x, ord=2) ** 2
        envelope = 0.0

        prox_term = prox_term.reshape(dim)
        assert prox_term.shape == x.shape

        return prox_term, envelope, linesearch_iters