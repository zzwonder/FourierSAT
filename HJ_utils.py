import numpy as np
from args import *
import time

def compute_prox_parallel(x0, polyStr, t=1e-1, delta=1e-1, int_samples=int(1e4), alpha=1.0, linesearch_iters=0):
    import torch

    assert x0.ndim == 1

    device = 'cuda:0'

    dim = len(x0)

    x0 = torch.tensor(x0)
    x0 = x0.view(1, dim)
    x0 = x0.to(device)
    linesearch_iters += 1
    standard_dev = np.sqrt(delta * t / alpha)

    # Sample y from a normal distribution centered at x with variance proportional to standard_dev
    x = standard_dev * torch.randn(int_samples, dim, device=device) + x0 # y has shape (n_samples x dim)
    assert x.shape == (int_samples, dim)

    # evaluate polynomial string at variable x
    start_time = time.time()
    fx = eval(polyStr)
    end_time = time.time()

    feval_time = end_time - start_time

    # print('feval_time = ', feval_time)

    z = -fx*(alpha/delta) # shape =  n_samples
    w = torch.softmax(z, dim=0) 

    assert z.shape == (int_samples, )

    softmax_overflow_check = (w < np.inf)
    if softmax_overflow_check.prod()==0.0:
        print('x0 = ', x0)
        print('z = ', z)
        print('w = ', w)
        alpha = 0.5*alpha
        return compute_prox_parallel(x0, polyStr, t=t, delta=delta, int_samples=int_samples, alpha=alpha, linesearch_iters=linesearch_iters, device=device)
    else:
        prox_term = torch.matmul(w.t(), x)
        prox_term = prox_term.view(-1,1)

        prox_overflow = (prox_term < np.inf)
        if prox_overflow.prod() == 0.0:
            print('prox overflowed: ', prox_term)
        assert(prox_overflow.prod() == 1.0)

        # find where fx is smallest and f(prox_term)
        min_index = torch.argmin(fx)
        f_best = fx[min_index]
        x_best = x[min_index, :].clone()
        assert x_best.shape == (dim, )

        x = prox_term.view(1,-1).clone()
        f_prox = eval(polyStr)
        # print('f_prox = ', f_prox, ', f_best = ', f_best)

        if f_best < f_prox:
            prox_term = x_best.view(dim,1)
        
        envelope = 0.0

        prox_term = prox_term.view(dim)
        prox_term = prox_term.cpu().numpy()

        return prox_term, envelope, linesearch_iters

def compute_prox(x, args, f, t=1e-1, delta=1e-2, int_samples=int(1e4), alpha=1.0, linesearch_iters=0):
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
        return compute_prox(x, args, f, t=t, delta=delta, int_samples=int_samples, alpha=alpha, linesearch_iters=linesearch_iters)
    else:
        prox_term = np.dot(w.T, y)  # Weighted average of y, shape = (dim,)

        # find index where z is minimum and obtain minimum between f(y_min) and f(prox_term)
        min_index = np.argmin(f_array)
        f_prox = f(prox_term[0], args)
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
