import importlib
from eeve.variable import Variable


def load_script(var: 'Union[Variable, str]', script_path: str):
    """Loads python script and stores to a variable
    
    Arguments:
        var {Union[Variable, str]} -- variable reference or variable name to store loaded script (module)
        script_path {str} -- path that script is located
    
    Returns:
        module -- The script (module) reference
    """
    # TODO: get script path and add to path environment variable
    script_name = script_path
    mod = importlib.import_module(script_name)
    if type(var) is Variable:
        var.value = mod
    else:
        return {var: mod}


def call_func(script_ref, func_name: str, *args, **kwargs):
    """Calls a function inside the module passed as parameter
    
    Arguments:
        script_ref {python_module} -- the reference to the module
        func_name {str} -- the name of the function to be called
    
    Returns:
        result -- contains the function result
    """
    return {'result': getattr(script_ref, func_name)(*args, **kwargs)}


actions = {'load script': {'run': load_script}, 'call function': {'run': call_func}}
