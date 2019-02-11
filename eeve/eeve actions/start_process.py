_DEFAULT_POOL = None


def threadpool(f, executor=None):
    global _DEFAULT_POOL
    from functools import wraps
    import concurrent.futures
    if _DEFAULT_POOL is None:
        _DEFAULT_POOL = concurrent.futures.ThreadPoolExecutor()

    @wraps(f)
    def wrap(*args, **kwargs):
        return (executor or _DEFAULT_POOL).submit(f, *args, **kwargs)

    return wrap


import subprocess

# made this way just as an example of a dict instead of a class

d = {'args': None, 'kwargs': None}


def init(self, *args, windowed=False, **kwargs):
    d['args'] = args
    d['kwargs'] = kwargs
    if windowed:
        kwargs['creationflags'] = subprocess.CREATE_NEW_CONSOLE


def run(self):
    print('start process:', d['args'], d['kwargs'])
    subprocess.Popen(d['args'], **d['kwargs'])


actions = {'start process': {'init': init, 'run': run}}
