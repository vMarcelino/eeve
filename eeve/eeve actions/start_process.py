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


class StartProcessAction:
    def __init__(self, *args, windowed=False, **kwargs):
        self.args = args
        self.kwargs = kwargs
        if windowed:
            kwargs['creationflags'] = subprocess.CREATE_NEW_CONSOLE

    def run(self):
        print('start process:', self.args, self.kwargs)
        subprocess.Popen(self.args, **self.kwargs)


actions = {'start process': StartProcessAction}