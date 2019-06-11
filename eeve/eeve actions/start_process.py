import subprocess


def run(*args, windowed: bool = False, **kwargs):
    """Starts a child program in a new process

    Starts a process with Popen. kwargs are passed directly to Popen
    
    Keyword Arguments:
        windowed {bool} -- Whether to start the new process in a new window or not (default: {False})
    """
    if windowed:
        kwargs['creationflags'] = subprocess.CREATE_NEW_CONSOLE

    print('start process:', args, kwargs)
    subprocess.Popen(args, **kwargs)


actions = {'start process': {'run': run}}
