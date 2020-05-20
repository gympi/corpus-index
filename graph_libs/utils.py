from functools import wraps
from time import time


def timing(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print(f'func: {f.__name__} elapsed time: {end - start:2.4f}')
        return result

    return wrap
