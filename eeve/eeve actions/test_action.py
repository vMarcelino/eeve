def init(*args, **kwargs):
    print('initialization args:', args, kwargs)


def run(*args, index=0, **kwargs):
    print(f'run args ({index}):', args, kwargs)
    try:
        index += 1
    except Exception as e:
        print(e)
        index = 1
    return {'index': index}


actions = {'test action': {'init': init, 'run': run}}
