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


class TimerTrigger:
    def __init__(self, action, t, *args, **kwargs):
        self.args = args
        self.action = action
        #print('Loadinnnnnnn')
        self.run(int(t))
        #print('loadeded')

    def unregister(self):
        self.callback = None

    @threadpool
    def run(self, t):
        import time
        while True:
            time.sleep(t)
            print('triggering action')
            self.action(time=t)


triggers = {'timer': TimerTrigger}