import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool

def abortable_worker(func, *args, **kwargs):
    timeout = kwargs.get('timeout',None)
    p = ThreadPool(1)
    res = p.apply_async(func,args=args)
    try:
           out = res.get(timeout)
           return out
    except multiprocessing.TimeoutError:
           res = so.OptimizeResult
           res.x = []
           return False,res,True

