def init(*args, **kwargs):
    print('initialization args:', args, kwargs)


def run(*args, **kwargs):
    print('run args:', args, kwargs)


actions = {'test action': {'init': init, 'run': run}}
