import os


def run(command: str):
    """Execute a command in a subshell
    
    Arguments:
        command {str} -- command to be executed
    
    Returns:
        return_code {int} -- the return code of the command executed
    """
    return_code = os.system(command)
    return {'return_code', return_code}


# actions = {'run': {'run': os.system}}  # could just do this but I want to comment
actions = {'run': {'run': run}}
